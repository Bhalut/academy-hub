resource "aws_kinesis_stream" "tracking_stream" {
  name             = var.stream_name
  shard_count      = 1
  retention_period = 24
}
