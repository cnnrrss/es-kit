#!/bin/bash

# Designed to build and run load locust load tests based on passed in environment variables
# then after a time stop the test, gather the states and then terminate
# Orginally designed to run on CI instances

# LOCUSTRUNTIME=60
# LOCUSTCOUNT=5
# LOCUSTHATCH=1
# LOCUSTFILE=locustfile_search.py

ip addr show
docker stop $(docker ps -a -q)
docker build -t locust_container -f Dockerfile.loadtest .
docker run -v $(pwd):/opt/app/ -w /opt/app/ -p 80:8089 locust_container locust -f $LOCUSTFILE --host=example.com &
sleep 10
curl --noproxy 127.0.0.1 'http://127.0.0.1:80/swarm' --data "locust_count=$LOCUSTCOUNT&hatch_rate=$LOCUSTHATCH"
sleep $LOCUSTRUNTIME
curl --noproxy 127.0.0.1 'http://127.0.0.1:80/stop'
curl -o requests.csv --noproxy 127.0.0.1 http://127.0.0.1:80/stats/requests/csv
curl -o distribution.csv --noproxy 127.0.0.1 http://127.0.0.1:80/stats/distribution/csv
curl -o exceptions.csv --noproxy 127.0.0.1 http://127.0.0.1:80/stats/exceptions/csv
docker stop $(docker ps -a -q)