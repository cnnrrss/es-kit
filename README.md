# ES Kit

A toolkit for ES cluster management and load testing

Kits:

github.com/taskrabbit/elasticsearch-dump


### Docker

Pull Image

`docker pull docker.elastic.co/elasticsearch/elasticsearch:7.4.2`

Single node cluster

`docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.4.2`

SSH in

`docker exec -it es01 /bin/bash`


### Get info from cluster

ssh in

```bash
echo $ES_JAVA_OPTS
-Xms512m -Xmx512m
```

Build and features info:

`curl -X GET "localhost:9200/_xpack?categories=build,features&pretty"`

[Cluster health](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-health.html)

`curl -X GET "localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s&pretty"`

Node stats

`curl -X GET "localhost:9200/_nodes/stats?pretty"`

Slow Queries Log

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

**Change cluster settings on running cluster with API**
`https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-update-settings.html`


Storage = throughput * events size * retention period.

If you decide to go cheap and combine the master and data nodes in a 3 hosts cluster, never use bulk indexing.

**Long-lived index**: You write code that processes data into one or more Elasticsearch indices and then updates those indices periodically as the source data changes. Some common examples are website, document, and e-commerce search.

**Elasticsearch indexing overhead**: The on-disk size of an index varies, but is often 10% larger than the source data. After indexing your data, you can use the _cat/indices API and pri.store.size value to calculate the exact overhead. The _cat/allocation API also provides a useful summary.

#### Calculate Storage

Source Data * (1 + Number of Replicas) * (1 + Indexing Overhead) / (1 - Linux Reserved Space) / (1 - Amazon ES Overhead) = Minimum Storage Requirement

Or you can use this simplified version:

Source Data * (1 + Number of Replicas) * 1.45 = Minimum Storage Requirement

#### Calculate Shards

(Source Data + Room to Grow) * (1 + Indexing Overhead) / Desired Shard Size = Approximate Number of Primary Shards

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

#### Warnings and Errors Observed

`OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was deprecated in version 9.0 and will likely be removed in a future release.`

### Settings to try

`logger.org.elasticsearch.transport: TRACE`

### Tune for indexing speed
- Disable refresh and replicas for initial loads
- Unset or increase the refresh interval
- Always use local storage, remote filesystems such as NFS or SMB should be avoided.

### Out of memory errors

Very often it is caused by something like a bad query, or indexing at a rate that is higher than the cluster is provisioned for.

### Heap dump

By default working directory of Elasticsearch. Can be explicit: `-XX:HeapDumpPath=<path>` in jvm.options

#### ES Circuit Breaker:

They are especially prone to issues for aggregations where it is difficult to estimate in advance the amount of memory that an aggregation will consume.

