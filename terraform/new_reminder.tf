
resource "aws_ecs_task_definition" "reminder_task" {
  family                = "new_reminder"
  container_definitions = file("./new_reminder.json")
  task_role_arn = "arn:aws:iam::612185335394:role/ecs_scheduler_task_role"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  cpu = 512
  memory = 1024
  execution_role_arn = "arn:aws:iam::612185335394:role/ecs_scheduler_execution_role"

}



resource "aws_cloudwatch_event_rule" "reminder_rule" {
  name        = "reminder"
  description = "Run new scheduler with reminders command"
  schedule_expression = "cron(15 12-22 ? * MON-FRI *)"
  
}

resource "aws_cloudwatch_event_target" "reminder_target" {
  target_id = "new_reminder_task"
  arn       = aws_ecs_cluster.scheduler_cluster.arn
  rule      = aws_cloudwatch_event_rule.reminder_rule.name
  role_arn  = "arn:aws:iam::612185335394:role/service-role/AWS_Events_Invoke_ECS"

  ecs_target {
    launch_type = "FARGATE"
    task_count          = 1
    task_definition_arn = aws_ecs_task_definition.reminder_task.arn
    network_configuration {
      subnets = [aws_subnet.public_subnet.id]
      assign_public_ip = true
      security_groups = [aws_security_group.allow_anything_for_lambda.id]
    }
  }
}