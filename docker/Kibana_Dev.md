# Run Kibana Locally

```bash
docker run -d --rm \
-p 9200:9200 \
-p 9300:9300 \
-e "discovery.type=single-node" \
-e "transport.host=127.0.0.1" \
--name elastic docker.elastic.co/elasticsearch/elasticsearch:7.4.2 && sleep 20
```

```bash
docker run -d --rm \
--link elastic:elastic-url \
-e "ELASTICSEARCH_URL=http://elastic-url:9200" \
-p 5601:5601 \
--name kibana docker.elastic.co/kibana/kibana:7.5.0 && sleep 20
```

`curl "http://localhost:9200/_count"`


`curl http://localhost:5601 --location`

docker run --link elastic:elasticsearch -p 5601:5601 kibana docker.elastic.co/kibana/kibana:7.5.0

#### Connect Elasticsearch Kibana Integration

1) Create index in Elasticsearch
    - Include Mappings: (keywords match exact values, text are searchable)
2) Create Kibana Index Patterns
3) Discover Index Pattern

https://www.elastic.co/guide/en/kibana/current/tutorial-define-index.html