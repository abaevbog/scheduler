read -p "Update SCHEDULER?" -n 1 -r
echo   
if [[ $REPLY =~ ^[Yy]$ ]]
then
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    $(aws ecr get-login --no-include-email)
    docker build -t scheduler ${DIR} 
    docker tag scheduler 612185335394.dkr.ecr.us-east-1.amazonaws.com/reminders_scheduler
    docker push 612185335394.dkr.ecr.us-east-1.amazonaws.com/reminders_scheduler
fi
