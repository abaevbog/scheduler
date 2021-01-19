read -p "Update SCHEDULER VERSION mongo?" -n 1 -r
echo   
if [[ $REPLY =~ ^[Yy]$ ]]
then
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    aws ecr get-login-password \
        --region us-east-1\
    | docker login \
        --username AWS \
        --password-stdin 612185335394.dkr.ecr.us-east-1.amazonaws.com
    docker build -t scheduler ${DIR} 
    docker tag scheduler 612185335394.dkr.ecr.us-east-1.amazonaws.com/scheduler
    docker push 612185335394.dkr.ecr.us-east-1.amazonaws.com/scheduler
fi
