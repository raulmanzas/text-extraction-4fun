resource "aws_iam_role" "poc-textract-role" {
  name               = "${local.common_prefix}-textract-role"
  assume_role_policy = <<-EOF
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Principal": {
                  "Service": "textract.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
          }
      ]
  }
  EOF
}

resource "aws_iam_role_policy_attachment" "poc-textract-role-policy" {
  role       = aws_iam_role.poc-textract-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonTextractServiceRole"
}
