
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
