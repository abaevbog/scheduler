read -p "Update SCHEDULER?" -n 1 -r
echo   
if [[ $REPLY =~ ^[Yy]$ ]]
then
    $(aws ecr get-login --no-include-email)
    docker build -t scheduler `pwd` 
    docker tag scheduler 612185335394.dkr.ecr.us-east-1.amazonaws.com/reminders_scheduler
    docker push 612185335394.dkr.ecr.us-east-1.amazonaws.com/reminders_scheduler
fi
