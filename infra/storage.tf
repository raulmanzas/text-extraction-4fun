
resource "aws_s3_account_public_access_block" "global_block_public_access" {
  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
}

resource "aws_s3_bucket" "documents_bucket" {
  bucket = "NAME-YOUR-BUCKET-HERE" # REPLACE THIS WITH YOUR BUCKET NAME
  acl    = "private"

  tags = {
    Env = local.env
  }
}
