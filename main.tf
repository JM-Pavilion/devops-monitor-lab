# --- 定义提供者 (Provider) ---
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# --- 配置 AWS 区域 (LocalStack 适配版) ---
provider "aws" {
  region                      = "ap-southeast-1"
  
  # 1. 注入虚拟钥匙（LocalStack 不检查钥匙真假，但 Terraform 必须得拿一把在手里）
  access_key                  = "test"
  secret_key                  = "test"

  # 2. 告诉 Terraform 别去联网查账号 ID 或元数据，直接连本地
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  # 3. 最关键的一步：把 EC2 服务的终点站指向你的 LocalStack (4566 端口)
  endpoints {
    ec2 = "http://localhost:4566"
  }
}

# --- 划地皮：创建一个最基础的 VPC ---
resource "aws_vpc" "jm_main_vpc" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "jm-local-vpc"
  }
}

# --- 在 VPC 里面划一块子网 (Subnet) ---
resource "aws_subnet" "jm_public_subnet" {
  # 关键：告诉 Terraform 这个子网属于刚才那个 VPC
  vpc_id            = aws_vpc.jm_main_vpc.id
  
  # 子网的网段必须包含在大网段里面
  cidr_block        = "10.0.1.0/24"
  
  # 设置可用区（LocalStack 模拟新加坡的 A 区）
  availability_zone = "ap-southeast-1a"

  tags = {
    Name = "jm-public-subnet-01"
  }
}

# 1. 互联网网关 (让 VPC 能看到外面的世界)
resource "aws_internet_gateway" "jm_igw" {
  vpc_id = aws_vpc.jm_main_vpc.id
  tags = { Name = "jm-igw" }
}

# 2. 路由表 (指路牌)
resource "aws_route_table" "jm_public_rt" {
  vpc_id = aws_vpc.jm_main_vpc.id
  route {
    cidr_block = "0.0.0.0/0" # 指向所有互联网流量
    gateway_id = aws_internet_gateway.jm_igw.id
  }
}

# 3. 关联 (把指路牌插在你的子网门口)
resource "aws_route_table_association" "jm_public_assoc" {
  subnet_id      = aws_subnet.jm_public_subnet.id
  route_table_id = aws_route_table.jm_public_rt.id
}

# --- 创建安全组：给你的服务器加个防火墙 ---
resource "aws_security_group" "jm_web_sg" {
  name        = "jm-web-sg"
  description = "Allow SSH and HTTP traffic"
  vpc_id      = aws_vpc.jm_main_vpc.id

  # 入站规则 (Ingress)：谁能进来？
  # 允许 SSH (22端口)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # 允许任何地方连接（实际生产中要限制IP）
  }

  # 允许 HTTP (80端口)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # 出站规则 (Egress)：里面的流量能去哪？
  # 通常允许所有流量出站
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # -1 代表所有协议
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "jm-web-sg"
  }
}


# --- 创建你的第一台 EC2 虚拟机 ---
# --- 1. 动态获取镜像 (这是 AWS SAA 考试必考知识点) ---
data "aws_ami" "latest_amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# --- 2. 修改你的 EC2 资源 ---
resource "aws_instance" "jm_web_server" {
  # 镜像 ID (在 LocalStack 中这只是个占位符，但在真实 AWS 中这代表 Amazon Linux 2023)
  ami           = data.aws_ami.latest_amazon_linux.id
  
  # 实例类型 (t2.micro 是免费套餐中最常用的)
  instance_type = "t2.micro"

  # 关键：把电脑放进我们刚才建好的房间里
  subnet_id     = aws_subnet.jm_public_subnet.id

  # 关键：给电脑配上刚才那个保安
  vpc_security_group_ids = [aws_security_group.jm_web_sg.id]

  # 自动分配公网 IP，这样我们才能从外面连它
  associate_public_ip_address = true


  # --- 嚼碎点：User Data (云服务器的启动脚本) ---
  # 这段脚本会在服务器第一次开机时自动执行
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y nginx
              systemctl start nginx
              systemctl enable nginx
              echo "<h1>Welcome JM! Your Monitoring System is coming soon...</h1>" > /usr/share/nginx/html/index.html
              EOF

  tags = {
    Name = "jm-monitor-host"
  }
}







