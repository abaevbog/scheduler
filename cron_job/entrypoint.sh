#!/bin/sh

# Fetch scheduler.sh with environment variables from S3 and run it to have
# them exported
#uncomment this is production
#aws s3 cp s3://basementremodeling-archive-12345/config/scheduler.sh .
# Run python runner
exec "$@"