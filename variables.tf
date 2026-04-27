variable "alicloud_access_key" {
  description = "Alibaba Cloud Access Key ID"
  type        = string
  sensitive   = true # 标记为敏感，Terraform 在日志里会打码
}

variable "alicloud_secret_key" {
  description = "Alibaba Cloud Secret Access Key"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "阿里云部署区域"
  default     = "cn-guangzhou"
}

variable "project_name" {
  description = "项目名称前缀"
  default     = "jm-monitor-lab"
}
