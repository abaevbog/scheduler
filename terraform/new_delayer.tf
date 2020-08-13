resource "aws_ecs_task_definition" "new_delayer_task" {
  family                = "new_delayer"
  container_definitions = file("./new_delayer.json")
  task_role_arn = "arn:aws:iam::612185335394:role/ecs_scheduler_task_role"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  cpu = 512
  memory = 1024
  execution_role_arn = "arn:aws:iam::612185335394:role/ecs_scheduler_execution_role"

}


resource "aws_cloudwatch_event_rule" "new_delayer_rule" {
  name        = "run_new_delayer"
  description = "Rule new scheduler with delayer command"
  schedule_expression = "cron(0 * ? * * *)"
  
}

resource "aws_cloudwatch_event_target" "new_ecs_delayer_task" {
  target_id = "run-new-delayer-task"
  arn       = aws_ecs_cluster.scheduler_cluster.arn
  rule      = aws_cloudwatch_event_rule.new_delayer_rule.name
  role_arn  = "arn:aws:iam::612185335394:role/service-role/AWS_Events_Invoke_ECS"

  ecs_target {
    launch_type = "FARGATE"
    task_count          = 1
    task_definition_arn = aws_ecs_task_definition.new_delayer_task.arn
    network_configuration {
      subnets = [aws_subnet.public_subnet.id]
      assign_public_ip = true
      security_groups = [aws_security_group.allow_anything_for_lambda.id]
    }
  }
}