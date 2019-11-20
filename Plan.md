# Plan

## Questions

Before resharding we must answer the following questions:
- Index growth by size (how many new docs are created every day/week/month?)
- Query volume, is this relatively constant? Do we expect it to grow in the future?
- Using your own document id or letting Elasticsearch assign it automatically?
- How has the index grown over time? It was mentioned you started adding more documents. How many were added, how quickly, how much more growth?
- When did you scale to four nodes?

### Reshard Process

- Take a [Snapshot](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-snapshots.html). First, you will have to create a "Snapshot Repository".

_Note_: I dont see any snapshot repos in the clust `/_cat/repositories?v`

```bash
curl -X PUT "localhost:9200/_snapshot/my_backup?pretty" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "my_backup_location"
  }
}
'
```

- _Optional_: Live Change Replication factor on K3 node

```bash
curl -X PUT "localhost:9200/k3-<date>/_settings?pretty" -H 'Content-Type: application/json' -d'
{
    "index" : {
        "number_of_replicas" : 1
    }
}
'
```

- Update index template

```bash
curl -X PUT "localhost:9200/_template/all" -H 'Content-Type: application/json' -d'
{
  "template": "*",
  "settings": {
    "number_of_shards": 4,
    "number_of_replicas": 1
  }
}
```

- Create new index with new number of shards, initially 0 replication (we'll change this later, and refresh interval set to -1, since we don’t need to query that index yet)
  - Check mappings. To assign specific data types to individual fields, the mapping must be created when the index is created

TODO: Spin up a new set of nodes? This incurs cost, but may be the safest choice.

```bash
curl -X PUT "localhost:9200/k3-<date>?pretty" -H 'Content-Type: application/json' -d'
{
    "settings" : {
        "index" : {
            "number_of_shards" : 4,
            "number_of_replicas" : 0
        }
    }
}
'
```

Wait for active shards.... response should look like
```json
{
    "acknowledged": true,
    "shards_acknowledged": true
}
```

- Migrate docs via bulk operations
  - Read all the docs in the old index (copy) to the new index
  - Do a scan on the source index and bulk import to the target index. Use [scrolling](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#request-body-search-scroll).
    - Require some form of bucketing because scoll may hold on to segments.
    - Bulk is risky with few nodes
- Change the index alias. Now all queries are served by the target index.
- Turn off double writing.
- Close the source index, freeing up resources.
- Maintain the source index on disk for a full day, just in case.

## Maintenance

#### Minor Elasticsearch upgrade to a new version. (See ansible dir)
- Disable shard allocation on the cluster
- Run an index flush sync
- Upgrade Elasticsearch to a new version
- Restart the Elasticsearch process
- Wait for the node to rejoin the cluster
- Enable shard allocation on the cluster
- Wait for the Elasticsearch cluster state to become green

#### Restart of Elasticsearch process to set a new configuration in production.
- Disable shard allocation on the cluster
- Run an index flush sync
- Restart the Elasticsearch process
- Wait for the node to rejoin the cluster
- Enable shard allocation on the cluster
- Wait for the Elasticsearch cluster state to become green
