read -p "Update SCHEDULER VERSION 2?" -n 1 -r
echo   
if [[ $REPLY =~ ^[Yy]$ ]]
then
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    $(aws ecr get-login --no-include-email)
    docker build -t scheduler ${DIR} 
    docker tag scheduler 612185335394.dkr.ecr.us-east-1.amazonaws.com/scheduler_v2
    docker push 612185335394.dkr.ecr.us-east-1.amazonaws.com/scheduler_v2
fi
