resource "aws_apigatewayv2_api" "tracking_api" {
  name          = "TrackingAPI"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "prod" {
  api_id      = aws_apigatewayv2_api.tracking_api.id
  name        = "prod"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "alb_integration" {
  api_id           = aws_apigatewayv2_api.tracking_api.id
  integration_type = "HTTP_PROXY"
  integration_uri  = "http://${aws_lb.tracking_alb.dns_name}"
}

resource "aws_apigatewayv2_route" "root_route" {
  api_id    = aws_apigatewayv2_api.tracking_api.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.alb_integration.id}"
}
