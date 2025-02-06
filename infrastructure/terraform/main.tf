provider "aws" {
  region = "us-east-1"
}

module "network" {
  source = "./vpc.tf"
}

module "ecs" {
  source          = "./ecs.tf"
  cluster_name    = "tracking-cluster"
  service_name    = "tracking-service"
  container_image = "<AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/tracking-service:latest"
  subnet_ids      = module.network.public_subnets
}

module "dynamodb" {
  source     = "./dynamodb.tf"
  table_name = "tracking-events"
}

module "kinesis" {
  source      = "./kinesis.tf"
  stream_name = "tracking-data"
}

module "alb" {
  source         = "./alb.tf"
  vpc_id         = module.network.vpc_id
  public_subnets = module.network.public_subnets
}

module "api_gateway" {
  source       = "./api_gateway.tf"
  alb_dns_name = module.alb.alb_dns_name
}
