### Stats

Bravo:
- avg doc size: 17.2kb

Prod:
- \# of docs: 2.2mil
- \# of docs deleted: 1.43mil
- avg doc size: 24.5kb
- avg shard size 301.mb
- primary storage size: 5.2gb / 4 == 1.3gb per shard.. should be good and room to scale
- total.store.size: 20.8gb
- \# of shards: 4
- \# of replicas: 3 <- can we change to 1?
- \# active primaries: 4
- \# of total shards: 16 ((4 * 3) + 4)
- 1 node per server
- 17x more writes than reads (13mil writes, 790k reads)

**Best Practices**
- [x] Is load balancer set up to round robin?
- [ ] Doc vals > field data (Def guide p.493)
- [ ] Preloading fielddata
- [x] \_id fields
- [x] not using too much field data
	- `"doc_values" : true` by default for every possible field
- [ ] Mapping Explosion _TBD_
- [ ] Reduce replication for write heavy workloads
- [ ] Avoid scripting in searches _TBD_
- [ ] Avoid deep dggregations _TBD_
- [ ] Using the string keyword type for identifiers [Link](https://www.elastic.co/guide/en/elasticsearch/reference/master/tune-for-search-speed.html)
- [ ] Don't return large result sets (If necessary, use [Scroll API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#request-body-search-scroll))
- [X] Batch index 1,000 to 5,000 docs at a time. (request size 5-15MB, at 17.2kb ~500 docs) `17.2k * 500 docs = 8.3mb`. I took an example from put_requests_log and saw bulk update of 96kb on only ~20docs. Can we bulk more? **Not at this time**
- [ ] Cache script queries and pass parameters. Scripts are compiled and cached for faster execution. If the same script can be used, just with different parameters provider, it is preferable to use the ability to pass parameters to the script itself, for example: 
	- Caching large queries can crash cluster, how about just script queries?

### Potential Solutions
- GC Tuning
	- GCMaxPauseMillis
	- `GCNewRatio=3` (Modifying NewRation may be a good option to tune for latency since the GC time is the shorter even though the New area size is smaller)
- Analyze and benchmark node / sharding / replication strategies
	- 4 node split brain problem
	- K3 index change replicas from 3 to 1 (this will reduce total shards from 16 to 8)
- Understand data loss tolerance and benchmark strategies
	- Are we able to use G1GC which is tuned specifically for large heap sizes >4GB but can sometimes lead to data loss.
	- Can we disable replication during reindexing?
	(If index can be built quickly on demand from external db is risk of potential data loss acceptable?)
- Query optimization
- Seeing issues such as QueryPhaseExecutionException
- Some organizations need blisteringly fast responses and opt to simply add more nodes. Other organizations are limited by budget and choose doc values and approximate aggregations.

If you only need 8 GB letting the heap grow to 18 GB can make performance worse, not better.

### Quick wins
- On k3 index change replicas from 3 to 1 (this will reduce total shards from 16 to 8)

- Improve reindexing task
	- Rollover daily indexes
	- Be sure that the shards for the index you're ingesting into are distributed evenly across the data nodes
		`k * (number of data nodes)` where k is the number of shards per node
	- Increase refresh_interval to 60 seconds or more
	- Experiment to find the optimal bulk request size (5mb - 15mb)
	- Change replica count to zero during reindex
		- If a node fails while replicas are disabled, you might lose data. Only disable replicas if you can tolerate data loss for an hour or two.
	- Use an instance type that has SSD instance store volumes, such as I3
	- Reduce response size
	- Increase the value of index.translog.flush_threshold_size
	- Disable the _all_ field on mapping for index

### Bulk requests

I would recommend sending larger bulk requests. A common recommendation is that each bulk request should be around 5MB in size.

**Long-lived index**: You write code that processes data into one or more Elasticsearch indices and then updates those indices periodically as the source data changes. Some common examples are website, document, and e-commerce search.

**Elasticsearch indexing overhead**: The on-disk size of an index varies, but is often 10% larger than the source data. After indexing your data, you can use the _cat/indices API and pri.store.size value to calculate the exact overhead. The _cat/allocation_ API also provides a useful summary.

If you decide to go cheap and combine the master and data nodes in a 3 hosts cluster, never use bulk indexing.

Get specific product:

```bash
curl -X GET "localhost:9200/<index>/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "_id": 1859587 } }
      ]
    }
  }
}
'
```

##### Set ES_HEAP_SIZE

In ubuntu/centOS

`/etc/sysconfig/elasticsearch`


`/etc/init.d/elasticsearch`