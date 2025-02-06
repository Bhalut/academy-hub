output "vpc_id" {
  description = "ID de la VPC creada"
  value       = aws_vpc.tracking_vpc.id
}

output "public_subnet_ids" {
  description = "IDs de las subredes públicas"
  value       = aws_subnet.public_subnets[*].id
}

output "ecs_cluster_id" {
  description = "ID del clúster de ECS"
  value       = aws_ecs_cluster.tracking.id
}

output "ecs_service_name" {
  description = "Nombre del servicio de ECS"
  value       = aws_ecs_service.tracking.name
}

output "dynamodb_table_arn" {
  description = "ARN de la tabla de DynamoDB"
  value       = aws_dynamodb_table.tracking_events.arn
}

output "kinesis_stream_arn" {
  description = "ARN del stream de Kinesis"
  value       = aws_kinesis_stream.tracking_stream.arn
}

output "alb_dns_name" {
  description = "Nombre DNS del Application Load Balancer"
  value       = aws_lb.tracking_alb.dns_name
}

output "api_gateway_endpoint" {
  description = "URL del API Gateway"
  value       = aws_apigatewayv2_api.tracking_api.api_endpoint
}
