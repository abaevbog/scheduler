provider "aws" {
  version = "~> 2.0"
  region  = "us-east-1"
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


resource "aws_ecs_cluster" "scheduler_cluster" {
  name = "scheduler_cluster"
  capacity_providers = ["FARGATE"]
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


