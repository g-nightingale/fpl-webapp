variable "step_function_name" {
    description = "Step function name"
    type        = string
}

variable "definition" {
  description = "JSON definition for the AWS Step Function state machine"
  type        = string
  default     = <<EOF
{
  "Comment": "A simple AWS Step Functions state machine that orchestrates three lambda functions.",
  "StartAt": "FirstFunction",
  "States": {
    "FirstFunction": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
      "Next": "SecondFunction"
    },
    "SecondFunction": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
      "Next": "ThirdFunction"
    },
    "ThirdFunction": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
      "End": true
    }
  }
}
EOF
}

variable "secret_arn" {
  description   = "Arn of secret"
  type          = string
}
