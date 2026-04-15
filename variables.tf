variable "aws_region" {
  description = "AWS 部署的区域"
  default     = "ap-southeast-1"
}

variable "instance_type" {
  description = "EC2 实例规格"
  default     = "t3.medium"
}

variable "project_name" {
  description = "项目名称前缀"
  default     = "jm-lab"
}
