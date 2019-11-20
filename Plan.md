# Plan

## Re-sharding

Before resharding we must answer the following questions:
- Index growth by size (how many new docs are created every day/week/month?)
- Query volume, is this relatively constant? Do we expect it to grow in the future?
- 


### Process

- Create new index with new number of shards

```bash
curl -X PUT "localhost:9200/k3-<date>?pretty" -H 'Content-Type: application/json' -d'
{
    "settings" : {
        "index" : {
            "number_of_shards" : 4, 
            "number_of_replicas" : 1
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

Default for number_of_shards is one per node
Default for number_of_replicas is 1 (ie one replica for each primary shard)

- Migrate docs via bulk operations

Read all the docs in the old index (copy) to the new index

