# Indexing


- [ ] Can we shrink the unused indices to 1 shard?
	- Reduces some unneccesary overhead
- [x] Use Bulk:
	- [ ] Benchmark different doc sizes 200, 400, 500, 1000
- [x] Use multiple threads / workers
- [ ] Disable refresh interval and replicas for full load
	- `index.refresh_interval: -1` `index.number_of_replicas: 0`
	- This will temporarily put your index at risk since the loss of any shard will cause data loss, but at the same time indexing will be faster since documents will be indexed only once.
- [x] Disable swapping (confirmed)
- [x] Give more memory to filesystem 
	- [ ] Right now it has half, can we lower the heap size?
- [ ] Use ES auto generated IDs
	- Right now the product ID is coming from a different source
- [ ] Faster hardware
	- See [link](https://www.elastic.co/guide/en/elasticsearch/reference/5.4/tune-for-indexing-speed.html#_use_faster_hardware)
- [ ] Can we tweak requirements to fit the Rollover API?
- [ ] Consider seperating data nodes and aggregator nodes

https://blog.codecentric.de/en/2014/05/elasticsearch-indexing-performance-cheatsheet/

Mapping

### If your search requirements allow it, there is some room for optimization in the mapping definition of your index:

- By default, Elasticsearch stores the original data in a special `_source` field. If you do not need it, disable it.
- By default, Elasticsearch analyzes the input data of all fields in a special _all field. If you do not need it, disable it.
- If you are using the _source field, there is no additional value in setting any other field to `_stored`.
- If you are not using the `_source` field, only set those fields to `_stored` that you need to. Note, however, that using `_source` brings certain advantages, such as the ability to use the update API.
- For analyzed fields, do you need norms? If not, disable them by setting norms.enabled to false.
- Do you need to store term frequencies and positions, as is done by default, or can you do with less – maybe only doc numbers? Set 
`index_options` to what you really need, as outlined in the string core type description.
- For analyzed fields, use the simplest analyzer that satisfies the requirements for the field. Or maybe you can even go with not_analyzed?
- Do not analyze, store, or even send data to Elasticsearch that you do not need for answering search requests. In particular, double-check the content of mappings that you do not define yourself (e.g., because a tool like Logstash generates them for you).


MEMORY:
INDEX_BUFFER_SIZE: 50% (INSTEAD OF 10%)
INDEX: STORE:
THROTTLE:
TYPE : "NONE" (AS FAST AS YOUR SSD CAN GO)
TRANSLOG: DISABLE_FLUSH: TRUE
REFRESH_INTERVAL: -1 (INSTEAD OF 1S) INDICES:
STORE: THROTTLE:
MAX_BYTES_PER_SEC: "2GB"