provider "aws" {
  region = "us-west-1"
}

locals {
  common_prefix = "poc-docs"
  env           = "poc-textract-docs"
}
