# Terraform does not support fifo sns topics right now, so both queue and topic
# have to be standard here
resource "aws_sqs_queue" "poc-queue" {
  name = "${local.common_prefix}-super-queue"

  tags = {
    Env = local.env
  }
}

resource "aws_sns_topic" "poc-topic" {
  name = "AmazonTextract-super-topic" # this prefix is required by aws

  tags = {
    Env = local.env
  }
}

resource "aws_sns_topic_subscription" "poc-topic-subscription" {
  topic_arn = aws_sns_topic.poc-topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.poc-queue.arn
}

resource "aws_sqs_queue_policy" "policy_allow_fanout_on_queue" {
  queue_url = aws_sqs_queue.poc-queue.id
  policy    = <<POLICY
  {
      "Statement": [
          {
              "Effect": "Allow",
              "Principal": {
                  "Service": "sns.amazonaws.com"
              },
              "Action": "sqs:SendMessage",
              "Resource": "${aws_sqs_queue.poc-queue.arn}",
              "Condition": {
                  "ArnEquals": {
                      "aws:SourceArn": "${aws_sns_topic.poc-topic.arn}"
                  }
              }
          }
      ]
  }
  POLICY
}
