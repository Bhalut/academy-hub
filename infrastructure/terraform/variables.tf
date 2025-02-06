variable "region" {
  description = "Región de AWS donde se desplegarán los recursos"
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "Nombre del clúster de ECS"
  type        = string
  default     = "tracking-cluster"
}

variable "service_name" {
  description = "Nombre del servicio de ECS"
  type        = string
  default     = "tracking-service"
}

variable "container_image" {
  description = "URI de la imagen del contenedor en ECR"
  type        = string
}

variable "dynamodb_table_name" {
  description = "Nombre de la tabla de DynamoDB"
  type        = string
  default     = "tracking-events"
}

variable "kinesis_stream_name" {
  description = "Nombre del stream de Kinesis"
  type        = string
  default     = "tracking-data"
}

variable "vpc_cidr" {
  description = "CIDR block para la VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "Lista de CIDR blocks para las subredes públicas"
  type = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "Lista de zonas de disponibilidad para las subredes"
  type = list(string)
  default = ["us-east-1a", "us-east-1b"]
}

variable "ecs_task_cpu" {
  description = "CPU asignada a la tarea de ECS"
  type        = number
  default     = 256
}

variable "ecs_task_memory" {
  description = "Memoria asignada a la tarea de ECS"
  type        = number
  default     = 512
}

variable "desired_count" {
  description = "Número deseado de instancias del servicio ECS"
  type        = number
  default     = 2
}
