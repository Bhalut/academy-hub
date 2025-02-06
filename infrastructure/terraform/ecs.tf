resource "aws_ecs_cluster" "tracking" {
  name = var.cluster_name
}

resource "aws_ecs_task_definition" "tracking" {
  family             = var.service_name
  requires_compatibilities = ["FARGATE"]
  network_mode       = "awsvpc"
  cpu                = "256"
  memory             = "512"
  execution_role_arn = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name   = var.service_name
      image  = var.container_image
      cpu    = 256
      memory = 512
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ],
      environment = [
        { "name" : "ENVIRONMENT", "value" : "production" },
        { "name" : "DYNAMODB_TABLE", "value" : "tracking-events" },
        { "name" : "KINESIS_STREAM", "value" : "tracking-data" }
      ],
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "ecs-logs-tracking"
          awslogs-region        = "us-east-1"
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "tracking" {
  name            = var.service_name
  cluster         = aws_ecs_cluster.tracking.id
  task_definition = aws_ecs_task_definition.tracking.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets = var.subnet_ids
    security_groups = [aws_security_group.ecs_sg.id]
  }
}
