# ES Kit

A toolkit for ES cluster management and load testing

### Docker

Pull Image

```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.4.2
```

Single node cluster

```bash
docker run -p 9200:9200 -p 9300:9300 \
-e "discovery.type=single-node" \
docker.elastic.co/elasticsearch/elasticsearch:7.4.2
```

SSH in to the docker container

`docker exec -it es01 /bin/bash`

### Tools

- Curator: maintenance tool [link](https://github.com/elastic/curator/blob/master/docs/asciidoc/about.asciidoc#features)
- Python: official py client [link](https://github.com/elastic/elasticsearch-py))
- Ansible: automation [link](https://github.com/elastic/ansible-elasticsearch)
- Dump: tool, requires node js [link](https://github.com/taskrabbit/elasticsearch-dump)

### Get info from cluster

**Build info**:

`curl -X GET "localhost:9200/_xpack?categories=build,features&pretty"`

[Cluster health](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-health.html)

`curl -X GET "localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s&pretty"`

**Cat API**: (nodes, indices, cluster, segments, etc...)

**Enable Slow Queries Log**

```bash
PUT /index/_settings
{
    "index.search.slowlog.threshold.query.warn: 1s",
    "index.search.slowlog.threshold.query.info: 500ms",
    "index.search.slowlog.threshold.query.debug: 1500ms",
    "index.search.slowlog.threshold.query.trace: 300ms",
    "index.search.slowlog.threshold.fetch.warn: 500ms",
    "index.search.slowlog.threshold.fetch.info: 400ms",
    "index.search.slowlog.threshold.fetch.debug: 300ms",
    "index.search.slowlog.threshold.fetch.trace: 200ms"
}
```

### Config

3 settings:

- `elasticsearch.yml` for configuring Elasticsearch
- `jvm.options` for configuring Elasticsearch JVM settings
- `log4j2.properties` for configuring Elasticsearch logging

See [Scaling](./Scaling.md) for more info

### Caching

Shard request cache

- Most queries that use now (see Date Math) cannot be cached

Cache can be expired manually

```bash
curl -X POST "localhost:9200/kimchy,elasticsearch/_cache/clear?request=true&pretty"
```

Enabling and disabling caching per request edit (overrides index setting)

```bash
curl -X GET "localhost:9200/my_index/_search?request_cache=true&pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "popular_colors": {
      "terms": {
        "field": "colors"
      }
    }
  }
}
'
```