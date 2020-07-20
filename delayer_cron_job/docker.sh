read -p "Update DELAYER?" -n 1 -r
echo   
if [[ $REPLY =~ ^[Yy]$ ]]
then
    $(aws ecr get-login --no-include-email)
    docker build -t delayer . 
    docker tag delayer 612185335394.dkr.ecr.us-east-1.amazonaws.com/delayer_scheduler
    docker push 612185335394.dkr.ecr.us-east-1.amazonaws.com/delayer_scheduler
fi