provider "aws" {
  version = "~> 2.0"
  region  = "us-east-1"
}

resource "aws_vpc" "scheduler_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "Scheduler VPC"
    Application = "Scheduler"
    Deployed_by = "Terraform"
  }  
}

resource "aws_subnet" "public_subnet" {
  vpc_id     = aws_vpc.scheduler_vpc.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true
  tags = {
    Name = "Public subnet"
    Application = "Scheduler"
    Deployed_by = "Terraform"
  }
}

resource "aws_internet_gateway" "scheduler_vpc_gateway" {
  vpc_id = aws_vpc.scheduler_vpc.id

  tags = {
    Name = "Scheduler VPC IG"
    Application = "Scheduler"
    Deployed_by = "Terraform"
  }
}


resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.scheduler_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.scheduler_vpc_gateway.id
  }
  tags = {
    Name = "Scheduler route table"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.route_table.id
}

resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.scheduler_vpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "Private subnet"
    Application = "Scheduler"
    Deployed_by = "Terraform"
  }
}
resource "aws_subnet" "private_subnet_two" {
  vpc_id     = aws_vpc.scheduler_vpc.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "Second Private subnet"
    Application = "Scheduler"
    Deployed_by = "Terraform"
  }
}

resource "aws_security_group" "allow_anything_for_lambda" {
  name        = "scheduler allow_https"
  description = "Allow https inbound traffic"
  vpc_id      = aws_vpc.scheduler_vpc.id
  lifecycle { 
    create_before_destroy = true 
    }
  ingress {
    description = "Anything into VPC"
    to_port     = 0
    from_port = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    to_port     = 0
    from_port = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "scheduler allow_https"
    Application = "Scheduler"
    Deployed_by = "Terraform"
    Used_by = "lambda function that talks to db"
  }
}


resource "aws_security_group" "scheduler_db_group" {
  name        = "scheduler db group"
  description = "Allow tcp traffic from SG allow_anything_for_lambda"
  vpc_id      = aws_vpc.scheduler_vpc.id

  ingress {
    description = "allow DB traffic from lambda"
    to_port     = 5432
    from_port = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    security_groups = [aws_security_group.allow_anything_for_lambda.id]
  }

  egress {
    to_port     = 0
    from_port = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "scheduler_db_group"
    Application = "Scheduler"
    Deployed_by = "Terraform"
    Used_by = "Scheduler database"
  }
}


variable "DB_credentials" {}

resource "aws_db_subnet_group" "private_subnets" {
  name       = "scheduler_subnet_group"
  subnet_ids = [aws_subnet.private_subnet.id, aws_subnet.private_subnet_two.id]

  tags = {
    Name = "Scheduler DB subnet group"
  }
}

resource "aws_db_instance" "scheduler_db"{
  allocated_storage    = 30
  storage_type         = "gp2"
  engine               = "postgres"
  instance_class       = "db.t3.small"
  name                 = "scheduler_database"
  username             = var.DB_credentials.username
  password             = var.DB_credentials.password
  backup_retention_period = 5
  db_subnet_group_name = aws_db_subnet_group.private_subnets.name
  maintenance_window = "Sun:00:00-Sun:03:00"
  backup_window = "03:01-03:31"
  vpc_security_group_ids = [aws_security_group.scheduler_db_group.id]
}



resource "aws_ecs_task_definition" "cron_task" {
  family                = "scheduler_cron"
  container_definitions = file("./container_def.json")
  task_role_arn = "arn:aws:iam::612185335394:role/ecs_scheduler_task_role"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  cpu = 512
  memory = 1024
  execution_role_arn = "arn:aws:iam::612185335394:role/ecs_scheduler_execution_role"

}

resource "aws_ecs_cluster" "scheduler_cluster" {
  name = "scheduler_cluster"
  capacity_providers = ["FARGATE"]
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

output "VPC" {
  value = aws_vpc.scheduler_vpc.id
}

output "Lambda_security_group" {
  value = aws_security_group.allow_anything_for_lambda.id
}

output "Public_Subnet" {
  value = aws_subnet.public_subnet.id
}


