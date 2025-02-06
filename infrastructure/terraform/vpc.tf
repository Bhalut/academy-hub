resource "aws_vpc" "tracking_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

resource "aws_subnet" "public_subnets" {
  count                   = 2
  vpc_id                  = aws_vpc.tracking_vpc.id
  cidr_block = element(["10.0.1.0/24", "10.0.2.0/24"], count.index)
  map_public_ip_on_launch = true
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}

output "vpc_id" {
  value = aws_vpc.tracking_vpc.id
}

output "public_subnets" {
  value = aws_subnet.public_subnets[*].id
}
