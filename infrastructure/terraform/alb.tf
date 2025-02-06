resource "aws_lb" "tracking_alb" {
  name               = "tracking-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.alb_sg.id]
  subnets            = var.public_subnets
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.tracking_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tracking_tg.arn
  }
}

resource "aws_lb_target_group" "tracking_tg" {
  name     = "tracking-tg"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}
