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
  region = var.aws_region # <--- 换成变量

  # 1. 注入虚拟钥匙（LocalStack 不检查钥匙真假，但 Terraform 必须得拿一把在手里）
  access_key = "test"
  secret_key = "test"

  # 2. 告诉 Terraform 别去联网查账号 ID 或元数据，直接连本地
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  # 3. 最关键的一步：把 EC2 服务的终点站指向你的 LocalStack (4566 端口)
  endpoints {
    ec2   = "http://127.0.0.1:4566"
    elb   = "http://127.0.0.1:4566"
    elbv2 = "http://127.0.0.1:4566" #负责 Target Group 和新版 LB
    s3    = "http://127.0.0.1:4566"
    iam   = "http://127.0.0.1:4566" # 这里不需要vpc，因为它已经包含在ec2里面了
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
  vpc_id = aws_vpc.jm_main_vpc.id

  # 子网的网段必须包含在大网段里面
  cidr_block = "10.0.1.0/24"

  # 设置可用区（LocalStack 模拟新加坡的 A 区）
  availability_zone = "ap-southeast-1a"

  tags = {
    Name = "jm-public-subnet-01"
  }
}

# 1. 互联网网关 (让 VPC 能看到外面的世界)
resource "aws_internet_gateway" "jm_igw" {
  vpc_id = aws_vpc.jm_main_vpc.id
  tags   = { Name = "jm-igw" }
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
    cidr_blocks = ["0.0.0.0/0"] # 允许全世界访问
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
    values = ["al2023-ami-*-x86_64"] # 自动匹配 Amazon Linux 2023 最新版
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# --- 2. 修改你的 EC2 资源 ---
resource "aws_instance" "jm_web_server" {
  # 镜像 ID (在 LocalStack 中这只是个占位符，但在真实 AWS 中这代表 Amazon Linux 2023)
  ami = data.aws_ami.latest_amazon_linux.id

  # 实例类型 (t2.micro 是免费套餐中最常用的)
  instance_type = var.instance_type

  # 关键：把电脑放进我们刚才建好的房间里
  subnet_id = aws_subnet.jm_public_subnet.id

  # 关键：给电脑配上刚才那个保安
  vpc_security_group_ids = [aws_security_group.jm_web_sg.id]

  # 自动分配公网 IP，这样我们才能从外面连它
  associate_public_ip_address = true

  # 只要说明书改了，就直接给我换台新电脑
  user_data_replace_on_change = true

  # 把“工牌”和“服务器”关联起来
  iam_instance_profile = aws_iam_instance_profile.jm_ec2_profile.name

  # --- 嚼碎点：User Data (云服务器的启动脚本) ---
  # 这段脚本会在服务器第一次开机时自动执行
  user_data = <<-EOF
            #!/bin/bash
            # 1. 更新系统并安装 Docker
            sudo yum update -y
            sudo amazon-linux-extras install docker -y
            
            # 2. 启动 Docker 服务
            sudo service docker start
            sudo usermod -a -G docker ec2-user
            
            # 3. 从云端超市拉取你的“预制菜”并运行
            # 我们把容器的 10000 端口映射到服务器的 80 端口（这样访问时就不用输端口号了）
            # 修改这一行，增加一个 -v 映射
            sudo docker run -d --restart always -p 80:10000 \
              -v /mnt/jm_data:/data \
              jminng/jm-monitor:latest


            # 新增的 EBS 挂载逻辑 （必须在 EOF 结束前）
            echo "Starting EBS volume configuration..."

            # 等待硬盘连接完成
            while [ ! -b /dev/sdh ]; do echo "Waiting for /dev/dsh..."
              sleep 5
            done

            # 如果硬盘没有文件系统，则格式化它
            if [ -z "$(lsblk -f /dev/sdh | grep ext4)" ]; then
              mkfs -t ext4 /dev/sdh
            fi

            # 创建挂载目录并挂载
            mkdir -p /mnt/jm_data
            mount /dev/sdh /mnt/jm_data

            # 确保开机自动挂载
            echo "/dev/sdh /mnt/jm_data ext4 defaults,nofail 0 2" >> /etc/fstab

            echo "EBS Volume mounted successfully at /mnt/jm_data"

            EOF

  # ... 原有的 docker 安装逻辑 ...

  tags = {
    Name = "${var.project_name}-host"
  }
}

# 1. 创建一个 10GB 的独立云硬盘
resource "aws_ebs_volume" "jm_data_vol" {
  availability_zone = "ap-southeast-1a" # 必须和 EC2 在同一个区
  size              = 10
  tags = {
    Name = "${var.project_name}-data-disk"
  }
}

# 2. 把硬盘“插”到 EC2 实例上
resource "aws_volume_attachment" "jm_ebs_att" {
  device_name = "/dev/sdh"
  volume_id   = aws_ebs_volume.jm_data_vol.id
  instance_id = aws_instance.jm_web_server.id
}

# --- 3. 输出部分 (必须独立放在外面) ---
output "ec2_public_ip" {
  value       = aws_instance.jm_web_server.public_ip
  description = "The public IP of the monitor server"
}

# 1. 创建一个唯一的 S3 存储桶
resource "aws_s3_bucket" "jm_assets_bucket" {
  bucket = "jm-lab-assets-20260419" # 注意：S3 的名字必须是全球唯一的

  tags = {
    Name        = "${var.project_name}-assets"
    Environment = "Dev"
  }
}

# 2. 开启版本控制（防止你手抖删错了，还能找回来）
resource "aws_s3_bucket_versioning" "jm_assets_versioning" {
  bucket = aws_s3_bucket.jm_assets_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}


# 创建一个角色，允许 EC2 替你干活
resource "aws_iam_role" "ec2_s3_access_role" {
  name = "jm_ec2_s3_access_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# 给“工牌”贴上“权限说明书”（Attachment）
resource "aws_iam_role_policy_attachment" "s3_readonly" {
  role       = aws_iam_role.ec2_s3_access_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

# 把“工牌”别在 EC2 的胸口上
resource "aws_iam_instance_profile" "jm_ec2_profile" {
  name = "jm_ec2_profile"
  role = aws_iam_role.ec2_s3_access_role.name
}





