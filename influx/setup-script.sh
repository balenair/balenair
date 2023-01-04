#!/bin/bash
set -e

if [ -z ${REPLICATION+x} ];
then
# install local dashboard and tasks
EXISTING_STACK_ID=$(influx stack list --name edge-replication |awk '{ print $1}')
if [ -z "$EXISTING_STACK_ID" ]; then 
EXISTING_STACK_ID=$(influx stacks init --hide-headers --stack-name edge-replication --stack-description "Replicate data from edge to cloud" |awk '{print $1}');
fi

echo "Found stack: $EXISTING_STACK_ID"
influx apply --force yes --file /docker-entrypoint-initdb.d/edge-replication.yml --stack-id $EXISTING_STACK_ID

# setup EDR to Cloud

if [ -z "$INFLUXDB_CLOUD_TOKEN" ]; then echo "You must add your remote cloud credentials to a .secrets file"; exit 1; fi

EXISTING_REPLICATION_ID=$(influx replication list --name edge-to-cloud --hide-headers |awk '{print $1}') 
if [ ! -z "$EXISTING_REPLICATION_ID" ]; then influx replication delete --id $EXISTING_REPLICATION_ID; fi

EXISTING_REMOTE_ID=$(influx remote list --name cloud --hide-headers |awk '{print $1}') 
if [ ! -z "$EXISTING_REMOTE_ID" ]; then influx remote delete --id ${EXISTING_REMOTE_ID}; fi

influx remote create --name cloud --org ${DOCKER_INFLUXDB_INIT_ORG} --remote-org-id ${INFLUXDB_CLOUD_ORG_ID} --remote-url ${INFLUXDB_CLOUD_HOST} --remote-api-token ${INFLUXDB_CLOUD_TOKEN}

REMOTE_ID=$(influx remote list --name cloud --hide-headers |awk '{print $1}') 
LOCAL_BUCKET_ID=$(influx bucket list --name downsampled --hide-headers |awk '{print $1}') 


influx replication create --name edge-to-cloud --org ${DOCKER_INFLUXDB_INIT_ORG} --remote-id $REMOTE_ID --local-bucket-id $LOCAL_BUCKET_ID --remote-bucket-id ${INFLUXDB_CLOUD_BUCKET_ID}

else
echo "No replication setup required"
fi

