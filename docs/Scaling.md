# Potential Solutions

### GC Tuning
- `XX:+UseG1GC` && `-XX:MaxGCPauseMillis=100`
- `GCNewRatio=3,4` 
	- Modifying NewRatio may be a good option to tune for latency since the GC time is the shorter even though the New area size is smaller). However, this significantly changes the JVM target usage and ratios.
- Xms Xmx smaller, how to we avoid out of memory? (fewer shards, less replication, etc..)

### Analyze and benchmark node / sharding / replication strategies
- 4 node split brain problem (can we do 3 nodes?)
- Shrink 5 shards to 4 on all indices, even less shards for the smaller indices?
- K3 index change replicas from 3 to 1 (this will reduce total shards from 16 to 8)

#### Understand data loss tolerance and benchmark strategies 
- Are we able to use G1GC which is tuned specifically for large heap sizes >4GB but can sometimes lead to data loss.
- Can we disable replication during reindexing?
	(If index can be built quickly on demand from external db is risk of potential data loss acceptable?)

### Query optimization
- Routing
- Seeing issues such as QueryPhaseExecutionException

- Relatively few fields

	- Defining too many fields in an index is a condition that can lead to a mapping explosion, which can cause out of memory errors and difficult situations to recover from. Particularly occurs when many heterogeneous documents are indexed. 
	
	https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping-limit-settings
	
	- The more fields a query_string or multi_match query targets, the slower it is. A common technique to improve search speed over multiple fields is to copy their values into a single field at index time, and then use this field at search time.

	https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-search-speed.html

	Index segmentation. There seems to be a common practice of many smaller indices with queries that operate across them (e.g. index prefix with a wildcard for the index name)

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

### Settings to try

`logger.org.elasticsearch.transport: TRACE`

- Tune for indexing speed (in this case)
	- [ ] Disable refresh and replicas for initial loads
	- [ ] Unset or increase the refresh interval
	- [ ] Always use local storage, remote filesystems such as NFS or SMB should be avoided.

- Out of memory errors: Very often it is caused by something like a bad query, or indexing at a rate that is higher than the cluster is provisioned for.

- Heap dump: By default working directory of Elasticsearch. Can be explicit: `-XX:HeapDumpPath=<path>` in jvm.options

- ES Circuit Breaker: They are especially prone to issues for aggregations where it is difficult to estimate in advance the amount of memory that an aggregation will consume.

- **Doc values**: loaded on disk instead of memory hence significantly lowering heap pressure. Caveat is they must be loaded at index time.


### Useful Links

- [Sizing](https://www.elastic.co/blog/found-sizing-elasticsearch)
- [Crashing](https://www.elastic.co/blog/found-crash-elasticsearch)
- [Understanding Memory Pressure](https://www.elastic.co/blog/found-understanding-memory-pressure-indicator)
- [Scaling @ Hipages](https://medium.com/hipages-engineering/scaling-elasticsearch-b63fa400ee9e)
- [Capacity Planning](https://www.elastic.co/guide/en/elasticsearch/guide/current/capacity-planning.html)

**Oracle**
- [CMS docs](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/cms.html)
- [G1GC docs](https://www.oracle.com/technical-resources/articles/java/g1gc.html#Imp)

**ES API**
- [CatNodesAPI](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-nodes.html)
- [RecoveryAPI](https://www.elastic.co/guide/en/elasticsearch/reference/master/cat-recovery.html)
- [ShrinkAPI](https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-shrink-index.html)

#### Warnings and Errors Observed

`OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was deprecated in version 9.0 and will likely be removed in a future release.`
