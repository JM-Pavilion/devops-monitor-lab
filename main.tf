# --- 1. 定义基础设施环境 ---
terraform {
  required_providers {
    alicloud = {
      source  = "aliyun/alicloud"
      version = "~> 1.209.0"
    }
  }
}

# --- 2. 动态获取镜像 (注意是 images 复数) ---
data "alicloud_images" "ubuntu" {
  name_regex  = "^ubuntu_22_04_x64" # 加上 _x64，确保是普通电脑架构
  owners      = "system"
  architecture = "x86_64"           # 明确指定架构，这就是解决问题的关键！
  most_recent = true
}

provider "alicloud" {
  region     = "cn-hangzhou" # 建议用杭州，国内最稳
}

# --- 2. 划出最简单的网络 (阿里云 ECS 必须有 VPC) ---
resource "alicloud_vpc" "jm_vpc" {
  vpc_name   = "jm-monitor-vpc"
  cidr_block = "172.16.0.0/12"
}

resource "alicloud_vswitch" "jm_vswitch" {
  vswitch_name = "jm-monitor-switch"
  vpc_id       = alicloud_vpc.jm_vpc.id
  cidr_block   = "172.16.1.0/24"
  zone_id      = "cn-hangzhou-j"
}

# --- 3. 配置安全组 (防火墙) ---
resource "alicloud_security_group" "jm_sg" {
  name   = "jm-monitor-sg"
  vpc_id = alicloud_vpc.jm_vpc.id
}

# 允许 80 端口访问（你的 Web 应用）
resource "alicloud_security_group_rule" "allow_http" {
  type              = "ingress"
  ip_protocol       = "tcp"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "80/80"
  priority          = 1
  security_group_id = alicloud_security_group.jm_sg.id
  cidr_ip           = "0.0.0.0/0"
}

# 允许 22 端口访问（SSH 登录）
resource "alicloud_security_group_rule" "allow_ssh" {
  type              = "ingress"
  ip_protocol       = "tcp"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "22/22"
  priority          = 1
  security_group_id = alicloud_security_group.jm_sg.id
  cidr_ip           = "0.0.0.0/0"
}

# --- 4. 创建 ECS 服务器 ---
resource "alicloud_instance" "jm_server" {
  instance_name              = "jm-monitor-host"
  availability_zone          = "cn-hangzhou-j"
  security_groups            = [alicloud_security_group.jm_sg.id]
  vswitch_id                 = alicloud_vswitch.jm_vswitch.id
  instance_type              = "ecs.e-c1m1.large" # 经济型 e 系列，可以用你的 300 元券
  system_disk_category       = "cloud_essd"
  image_id                   = data.alicloud_images.ubuntu.images[0].id # Ubuntu 系统
  
  # 分配公网 IP
  internet_max_bandwidth_out = 5

  # 开机自动装 Docker 并跑你的项目
  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io
              systemctl start docker
              systemctl enable docker
              # 拉取你的 Docker 镜像
              docker run -d --restart always -p 80:10000 jminng/jm-monitor:latest
              EOF
}

# --- 5. 告诉我们服务器的 IP ---
output "ecs_public_ip" {
  value = alicloud_instance.jm_server.public_ip
}

