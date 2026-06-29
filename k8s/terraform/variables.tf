variable "region" {
  description = "Alibaba Cloud deployment region"
  type        = string
  default     = "cn-hangzhou"
}

variable "project_name" {
  description = "Resource name prefix"
  type        = string
  default     = "jm-monitor"
}

variable "ecs_password" {
  description = "ECS instance root password"
  type        = string
  sensitive   = true
}
