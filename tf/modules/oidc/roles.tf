# IAM roles and permissions for the oidc module.
#
# Any block with 'resources = ["*"]' generally can't be tightened further due
# to constraints on the AWS side, but there might still be some small gains to
# be found by zooming in at high detail. We can continue to refine this data.
#
# https://docs.aws.amazon.com/service-authorization/latest/reference/reference.html

data "aws_iam_policy_document" "gha_oidc_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      identifiers = [aws_iam_openid_connect_provider.github.arn]
      type        = "Federated"
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values = concat(
        [
          for item in var.oidc_allowed :
          "repo:${item["org"]}/${item["repo"]}:pull_request"
        ],
        [
          for item in var.oidc_allowed :
          "repo:${item["org"]}/${item["repo"]}:ref:refs/heads/${item["branch"]}"
        ],
      )
    }
  }
}

data "aws_iam_policy_document" "gha_oidc_policy" {
  statement {
    effect = "Allow"
    actions = [
      "acm:AddTagsToCertificate",
      "acm:DescribeCertificate",
      "acm:ListTagsForCertificate",
    ]
    resources = [
      "arn:aws:acm:us-east-1:${var.aws_account}:certificate/*",
      "arn:aws:acm:${var.aws_region}:${var.aws_account}:certificate/*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "dynamodb:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "dynamodb:DeleteItem",
      "dynamodb:Get*",
      "dynamodb:PutItem",
    ]
    resources = [
      "arn:aws:dynamodb:${var.aws_region}:${var.aws_account}:table/${var.lock_table}",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "application-autoscaling:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "application-autoscaling:List*",
      "application-autoscaling:PutScalingPolicy",
      "application-autoscaling:RegisterScalableTarget",
      "application-autoscaling:TagResource",
    ]
    resources = [
      "arn:aws:application-autoscaling:${var.aws_region}:${var.aws_account}:*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "cloudfront:CreateDistributionWithTags",
      "cloudfront:CreateFunction",
      "cloudfront:CreateInvalidation",
      "cloudfront:CreateOriginAccessControl",
      "cloudfront:Describe*",
      "cloudfront:Get*",
      "cloudfront:List*",
      "cloudfront:PublishFunction",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "cloudwatch:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "cloudwatch:DeleteAlarms",
      "cloudwatch:DisableAlarmActions",
      "cloudwatch:EnableAlarmActions",
      "cloudwatch:Get*",
      "cloudwatch:List*",
      "cloudwatch:PutMetricAlarm",
      "cloudwatch:TagResource",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["arn:aws:cloudwatch:${var.aws_region}:${var.aws_account}:*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "ec2:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "ec2:AllocateAddress",
      "ec2:AssociateRouteTable",
      "ec2:AttachInternetGateway",
      "ec2:AuthorizeSecurityGroupEgress",
      "ec2:AuthorizeSecurityGroupIngress",
      "ec2:CreateFlowLogs",
      "ec2:CreateInternetGateway",
      "ec2:CreateNatGateway",
      "ec2:CreateRoute",
      "ec2:CreateRouteTable",
      "ec2:CreateSecurityGroup",
      "ec2:CreateSubnet",
      "ec2:CreateTags",
      "ec2:CreateVpcEndpoint",
      "ec2:ModifyVpcEndpoint",
      "ec2:DeleteVpcEndpoints",
      "ec2:RevokeSecurityGroupEgress",
    ]
    resources = [
      "arn:aws:ec2:${var.aws_region}:${var.aws_account}:*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "ecr:Describe*",
      "ecr:GetAuthorizationToken",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:BatchGetImage",
      "ecr:CompleteLayerUpload",
      "ecr:CreateRepository",
      "ecr:DeleteLifecyclePolicy",
      "ecr:Get*",
      "ecr:InitiateLayerUpload",
      "ecr:List*",
      "ecr:PutImage",
      "ecr:PutLifecyclePolicy",
      "ecr:TagResource",
      "ecr:UploadLayerPart",
    ]
    resources = [
      "arn:aws:ecr:${var.aws_region}:${var.aws_account}:*",
    ]
  }

  # statement {
  #   effect = "Allow"
  #   # tfsec:ignore:aws-iam-no-policy-wildcards
  #   actions = [
  #     "ecs:CreateCluster",
  #     "ecs:CreateService",
  #     "ecs:CreateTaskSet",
  #     "ecs:DeleteTaskSet",
  #     "ecs:DeregisterTaskDefinition",
  #     "ecs:Describe*",
  #     "ecs:List*",
  #     "ecs:PutClusterCapacityProviders",
  #     "ecs:RegisterTaskDefinition",
  #     "ecs:UpdateService",
  #     "ecs:UpdateServicePrimaryTaskSet",
  #   ]
  #   # tfsec:ignore:aws-iam-no-policy-wildcards
  #   resources = ["*"]
  # }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "elasticloadbalancing:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "elasticloadbalancing:AddTags",
      "elasticloadbalancing:CreateListener",
      "elasticloadbalancing:CreateLoadBalancer",
      "elasticloadbalancing:CreateTargetGroup",
      "elasticloadbalancing:Describe*",
      "elasticloadbalancing:ModifyLoadBalancerAttributes",
      "elasticloadbalancing:ModifyTargetGroupAttributes",
      "elasticloadbalancing:SetSecurityGroups",
    ]
    resources = [
      "arn:aws:elasticloadbalancing:${var.aws_region}:${var.aws_account}:*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "es:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "es:AddTags",
      "es:CreateDomain",
      "es:Get*",
      "es:List*",
      "es:UpdateDomainConfig",
    ]
    resources = [
      "arn:aws:es:${var.aws_region}:${var.aws_account}:*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "events:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "events:List*",
      "events:PutRule",
    ]
    resources = [
      "arn:aws:events:${var.aws_region}:${var.aws_account}:*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "iam:AttachRolePolicy",
      "iam:CreatePolicy",
      "iam:CreatePolicyVersion",
      "iam:CreateRole",
      "iam:CreateServiceLinkedRole",
      "iam:DeletePolicyVersion",
      "iam:Describe*",
      "iam:Get*",
      "iam:List*",
      "iam:GetOpenIDConnectProvider",
      "iam:PassRole",
      "iam:TagRole",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "kms:CreateGrant",
      "kms:CreateKey",
      "kms:Decrypt",
      "kms:Describe*",
      "kms:EnableKeyRotation",
      "kms:Get*",
      "kms:List*",
      "kms:PutKeyPolicy",
      "kms:TagResource",
    ]
    resources = [
      "arn:aws:kms:${var.aws_region}:${var.aws_account}:key/*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "logs:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "logs:CreateLogDelivery",
      "logs:DeleteLogDelivery",
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:Describe*",
      "logs:ListTags*",
      "logs:PutResourcePolicy",
      "logs:PutRetentionPolicy",
      "logs:TagLogGroup",
    ]
    resources = [
      "arn:aws:logs:${var.aws_region}:${var.aws_account}:*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "rds:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "rds:AddTagsToResource",
      "rds:CreateDBInstance",
      "rds:CreateDBParameterGroup",
      "rds:ModifyDBParameterGroup",
      "rds:CreateDBSubnetGroup",
      "rds:ListTags*",
    ]
    resources = [
      "arn:aws:rds:${var.aws_region}:${var.aws_account}:*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "route53:Describe*",
      "route53:Get*",
      "route53:List*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "s3:Describe*",
      "s3:List*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "s3:CreateBucket",
      "s3:DeleteObject",
      "s3:Get*",
      "s3:PutBucketAcl",
      "s3:PutBucketCORS",
      "s3:PutBucketLogging",
      "s3:PutBucketOwnershipControls",
      "s3:PutBucketPolicy",
      "s3:PutBucketPublicAccessBlock",
      "s3:PutBucketTagging",
      "s3:PutBucketVersioning",
      "s3:PutObject",
    ]
    resources = [
      "arn:aws:s3:::*${var.environment}-${var.aws_account}",
      "arn:aws:s3:::*${var.environment}-${var.aws_account}/*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "secretsmanager:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "secretsmanager:CreateSecret",
      "secretsmanager:Get*",
      "secretsmanager:PutSecretValue",
      "secretsmanager:TagResource",
    ]
    resources = [
      "arn:aws:secretsmanager:${var.aws_region}:${var.aws_account}:secret:${var.service}-secret-${var.environment}-*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "sfn:Describe*",
      "states:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "sfn:CreateStateMachine",
      "sfn:List*",
      "sfn:UpdateStateMachine",
      "states:List*",
    ]
    resources = [
      "arn:aws:states:${var.aws_region}:${var.aws_account}:stateMachine:*",
    ]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "sns:Describe*",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "sns:CreateTopic",
      "sns:Get*",
      "sns:List*",
      "sns:SetTopicAttributes",
      "sns:Subscribe",
      "sns:TagResource",
    ]
    resources = [
      "arn:aws:sns:${var.aws_region}:${var.aws_account}:*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "tag:GetResources",
    ]
    # tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    # tfsec:ignore:aws-iam-no-policy-wildcards
    actions = [
      "wafv2:Get*",
      "wafv2:List*",
      "wafv2:PutLoggingConfiguration",
    ]
    resources = [
      "arn:aws:wafv2:us-east-1:${var.aws_account}:global/*",
    ]
  }
}

locals {
  role_name   = "${var.service}-${var.gha_oidc_role_name}-${var.environment}"
  policy_name = "${var.service}-gha-oidc-policy-${var.environment}"
}

resource "aws_iam_role" "gha_oidc_role" {
  name               = local.role_name
  assume_role_policy = data.aws_iam_policy_document.gha_oidc_role.json

  tags = {
    Name = local.role_name
  }
}

resource "aws_iam_policy" "gha_oidc_policy" {
  name   = local.policy_name
  policy = data.aws_iam_policy_document.gha_oidc_policy.json

  tags = {
    Name = local.policy_name
  }
}

resource "aws_iam_role_policy_attachment" "gha_oidc_role" {
  role       = aws_iam_role.gha_oidc_role.name
  policy_arn = aws_iam_policy.gha_oidc_policy.arn
}

resource "aws_iam_role_policy_attachment" "ecs_full_access_policy_attachment" {
  role       = aws_iam_role.gha_oidc_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonECS_FullAccess"
}
