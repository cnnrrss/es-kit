# Plan


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
    - Require some form of bucketing because scroll may hold on to segments.
    - Bulk is risky with few nodes
- Change the index alias. Now all queries are served by the target index.
- Turn off double writing.
- Close the source index, freeing up resources.
- Maintain the source index on disk for a full day, just in case.

## Maintenance

### Change index resfresh interval

```bash
PUT /my_logs
{
  "settings": {
    "refresh_interval": "30s" 
  }
}
```

#### Segment Throttling
```bash
PUT /_cluster/settings
{
    "persistent" : {
        "indices.store.throttle.max_bytes_per_sec" : "100mb"
    }       
}
```

if we are doing bulk reindex and dont care about search at all
```bash
PUT /_cluster/settings
{
    "transient" : {
        "indices.store.throttle.type" : "none"
    } 
}
```

#### [Restart]

```bash
maprcli node services -name elasticsearch -nodes <space separated list of Elasticsearch nodes> -action restart
```

#### Minor Elasticsearch upgrade to a new version. (See ansible dir)
- Disable shard allocation on the cluster
- Run an index flush sync
- Upgrade Elasticsearch to a new version
- Restart the Elasticsearch process
- Wait for the node to rejoin the cluster
- Enable shard allocation on the cluster
- Wait for the Elasticsearch cluster state to become green

#### Change JVM settings
- Disable shard allocation on the cluster
- Run an index flush sync
- Update the jvm settings
- Restart the Elasticsearch process
- Wait for the node to rejoin the cluster
- Enable shard allocation on the cluster
- Wait for the Elasticsearch cluster state to become green

Also [see](https://www.elastic.co/guide/en/elasticsearch/reference/5.4/restart-upgrade.html)

#### Restart of Elasticsearch process to set a new configuration in production.
- Disable shard allocation on the cluster
- Run an index flush sync
- Restart the Elasticsearch process
- Wait for the node to rejoin the cluster
- Enable shard allocation on the cluster
- Wait for the Elasticsearch cluster state to become green

## Questions

Before resharding we must answer the following questions:
- Index growth by size (how many new docs are created every day/week/month?)
- Query volume, is this relatively constant? Do we expect it to grow in the future?
- Using your own document id or letting Elasticsearch assign it automatically?
- How has the index grown over time? It was mentioned you started adding more documents. How many were added, how quickly, - What is the refresh interval of the indices? Since we are doing a lot of updates, can we increase the refresh from default 1s to say... 30seconds? This can be done dynamically on a live index. At the very least this shuold be disabled during large indexes `-1` then when indexing is finished increase back to default.
how much more growth do you expect?
- When did you scale to four nodes?
  - Raising the refresh interval will also help with the explosive creation of segments. Automatic refresh process creates a new segment every second. Then each search must check every segment (p 166)
- Are we seeing this? Elasticsearch will log INFO-level messages stating now throttling indexing. If we're using SSDs we can increase the throttle from 20mb to 50 or 100 to trade   - We can use the optimize API but only if we stop updates on the index. (merges to a single segment.) (p 651, 595)
CPU and merge segs faster