resource "aws_ecs_cluster" "app" {
  name = "app"
}

resource "aws_ecs_service" "sun_api" {
  name                   = "sun_api"
  task_definition        = aws_ecs_task_definition.sun_api.arn
  cluster                = aws_ecs_cluster.app.id
  launch_type            = "FARGATE"
  enable_execute_command = true
  desired_count          = 1

  network_configuration {
    assign_public_ip = false

    security_groups = [
      aws_security_group.egress_all.id,
      aws_security_group.ingress_api.id,
    ]

    subnets = [
      aws_subnet.private_d.id,
      aws_subnet.private_e.id,
    ]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.sun_api.arn
    container_name   = "sun-api"
    container_port   = "9202"
  }
}

resource "aws_cloudwatch_log_group" "sun_api" {
  name = "/ecs/sun-api"
}

resource "aws_ecs_task_definition" "sun_api" {
  family     = "sun-api"
  depends_on = [aws_db_instance.sun-api]

  container_definitions = <<EOF
  [
    {
      "name": "sun-api",
      "image": "617542518433.dkr.ecr.us-east-1.amazonaws.com/breakable-toy-luke:latest",
      "portMappings": [
        {
          "containerPort": 9202
        }
      ],
      "environment": [
        {
            "name": "RDS_DB_NAME",
            "value": "${var.rds_db_name}"
        },
        {
            "name": "RDS_USERNAME",
            "value": "${var.rds_username}"
        },
        {
            "name": "RDS_PASSWORD",
            "value": "${var.rds_password}"
        },
        {
            "name": "RDS_HOSTNAME",
            "value": "${aws_db_instance.sun-api.address}"
        },
        {
            "name": "RDS_PORT",
            "value": "5432"
        }
        ],

      "command": ["-w", "1", "-b", "0.0.0.0:9202", "--reload", "--log-level", "info", "--error-logfile", "-", "--forwarded-allow-ips", "*", "-k", "gevent", "ebusserver.wsgi"],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-region": "us-east-1",
          "awslogs-group": "/ecs/sun-api",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
  EOF

  task_role_arn      = aws_iam_role.sun_api_task_role.arn
  execution_role_arn = aws_iam_role.sun_api_task_execution_role.arn

  # Minimum values for Fargate containers.
  cpu                      = 256
  memory                   = 512
  requires_compatibilities = ["FARGATE"]

  # Required for Fargate containers 
  network_mode = "awsvpc"
}

# This is the role under which ECS will execute our task, important
# as we add integrations with other AWS services later

# The assume_role_policy field works with the following aws_iam_policy_document to allow
# ECS tasks to assume this role we're creating.


resource "aws_iam_role" "sun_api_task_execution_role" {
  name               = "sun-api-task-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume_role.json
}

resource "aws_iam_role" "sun_api_task_role" {
  name                = "sun-api-task-role"
  assume_role_policy  = data.aws_iam_policy_document.ecs_task_assume_role.json
  managed_policy_arns = [aws_iam_policy.enable_execute_into.arn]
}



data "aws_iam_policy_document" "ecs_task_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# Normally prefer not to hardcode an ARN in Terraform, but ok since this is
# an AWS-managed policy
data "aws_iam_policy" "ecs_task_execution_role" {
  arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Attach the above policy to the execution role.
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role" {
  role       = aws_iam_role.sun_api_task_execution_role.name
  policy_arn = data.aws_iam_policy.ecs_task_execution_role.arn
}

resource "aws_iam_policy" "enable_execute_into" {
  name = "sesAppEnableExecuteInto"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssmmessages:CreateControlChannel",
          "ssmmessages:CreateDataChannel",
          "ssmmessages:OpenControlChannel",
          "ssmmessages:OpenDataChannel"
        ],
        Resource = "*"
      },
    ]
  })

}


resource "aws_lb_target_group" "sun_api" {
  name        = "sun-api"
  port        = 9202
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.app_vpc.id

  health_check {
    enabled = true
    path    = "/ping/"
  }

  depends_on = [aws_alb.sun_api]
}

resource "aws_alb" "sun_api" {
  name               = "sun-api-lb"
  internal           = false
  load_balancer_type = "application"

  subnets = [
    aws_subnet.public_d.id,
    aws_subnet.public_e.id,
  ]

  security_groups = [
    aws_security_group.http.id,
    aws_security_group.https.id,
    aws_security_group.egress_all.id,
  ]

  depends_on = [aws_internet_gateway.igw]
}

resource "aws_alb_listener" "sun_api_http" {
  load_balancer_arn = aws_alb.sun_api.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.sun_api.arn
  }
}

output "alb_url" {
  value = "http://${aws_alb.sun_api.dns_name}"
}
