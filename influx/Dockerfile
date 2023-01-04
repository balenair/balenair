FROM influxdb:latest

COPY ./edge-replication.yml /docker-entrypoint-initdb.d/edge-replication.yml
COPY ./setup-script.sh /docker-entrypoint-initdb.d/setup-script.sh