



resource "aws_ecs_task_definition" "cron_task" {
  family                = "scheduler_cron"
  container_definitions = file("./scheduler_container.json")
  task_role_arn = "arn:aws:iam::612185335394:role/ecs_scheduler_task_role"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  cpu = 512
  memory = 1024
  execution_role_arn = "arn:aws:iam::612185335394:role/ecs_scheduler_execution_role"

}


resource "aws_cloudwatch_event_rule" "scheduler_scheduler" {
  name        = "run_cron_tasks_on_ecs"
  description = "Rule to trigger runs on ecs"
  schedule_expression = "cron(0 12-22 ? * MON-FRI *)"
  
}

resource "aws_cloudwatch_event_target" "ecs_scheduled_task" {
  target_id = "run-scheduled-scheduler-task"
  arn       = aws_ecs_cluster.scheduler_cluster.arn
  rule      = aws_cloudwatch_event_rule.scheduler_scheduler.name
  role_arn  = "arn:aws:iam::612185335394:role/service-role/AWS_Events_Invoke_ECS"

  ecs_target {
    launch_type = "FARGATE"
    task_count          = 1
    task_definition_arn = aws_ecs_task_definition.cron_task.arn
    network_configuration {
      subnets = [aws_subnet.public_subnet.id]
      assign_public_ip = true
      security_groups = [aws_security_group.allow_anything_for_lambda.id]
    }
  }
}