# Notes

k3

- # of docs: 2,224,357
	- # of docs deleted: 1,143,301
- store.size: 20.8gb
- pri.stor.size: 5.2gb
- # of shards: 4
- # of replicas: 1
- # active primaries: 4
- # of total shards: 16 ((4 * 3) + 4)
- 1 node per server

### Potential Solutions
- GC Tuning
	- GCMaxPauseMillis
	- GCNewRatio=3,4 (Modifying NewRation may be a good option to tune for latency since the GC time is the shorter even though the New area size is smaller)
- Analyze and benchmark node / sharding / replication strategies
	- 4 node split brain problem
	- K3 index change replicas from 3 to 1 (this will reduce total shards from 16 to 8)
- Understand data loss tolerance and benchmark strategies 
	- Are we able to use G1GC which is tuned specifically for large heap sizes >4GB but can sometimes lead to data loss.
	- Can we disable replication during reindexing?
	(If index can be built quickly on demand from external db is risk of potential data loss acceptable?)
- Query optimization
-   Seeing issues such as QueryPhaseExecutionException

If you only need 8 GB letting the heap grow to 18 GB can make performance worse, not better.

### Quick wins 
- On k3 index change replicas from 3 to 1 (this will reduce total shards from 16 to 8)

```bash
# Set the number of shards (splits) of an index (5 by default):
index.number_of_shards: 4

# Set the number of replicas (additional copies) of an index (1 by default):
index.number_of_replicas: 1
```

- Experiment with GCPauseMillis

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

Bravo:
- avg doc size: 17.2kb

Prod:
- avg doc size: 24.5kb
- avg shard size 301.mb

### Quantitative Cluster Sizing
- Node (server in this case)
- Index (where docs live), contains multiple shards
- Shard: typically a few per node. 2 types (primaries, replicas)
	- Primary: write ops, (index, re-index, deletes, also reads)
	- Replica: high avail, read though-put (replica do just as much work as primaries)
		- doc being indexed will be indexed _n_ many times per replica

How big shard? How many? How many per node? How many active per node?
Which fields are searchable?
Multi-fields?
Heavy terms agg over 90 days of data?
Sustained indexing throughout the day, or a peak?

Determine breaking point of a shard

curl -X GET "localhost:9200/k3_20191108163756/_stats?pretty"
