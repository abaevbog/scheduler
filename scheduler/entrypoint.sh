#!/bin/sh

# Fetch scheduler.sh with environment variables from S3 and run it to have
# them exported

aws s3 cp s3://basementremodeling-archive-12345/config/scheduler.conf . > /dev/null
# Run python runner
python main.py $@