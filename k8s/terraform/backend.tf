terraform {
  backend "oss" {
    bucket              = "jm-terraform-state"
    prefix              = "dev/"
    key                 = "terraform.tfstate"
    region              = "cn-hangzhou"
    endpoint            = "oss-cn-hangzhou.aliyuncs.com"
    
    # 这里记得同步更新为下划线版
    tablestore_endpoint = "https://jm-tf-lock.cn-hangzhou.ots.aliyuncs.com"
    tablestore_table    = "terraform_lock_table" 
  }
}
