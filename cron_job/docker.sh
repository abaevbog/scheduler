docker build -t scheduler . 
docker tag scheduler 612185335394.dkr.ecr.us-east-1.amazonaws.com/reminders_scheduler
docker push 612185335394.dkr.ecr.us-east-1.amazonaws.com/reminders_scheduler