## Mappings 

Mapping is the process of defining how a document, and the fields it contains, are stored and indexed. For instance, use mappings to define:

- which string fields should be treated as full text fields.
- which fields contain numbers, dates, or geolocations.
- the format of date values.
- custom rules to control the mapping for dynamically added fields.


### Mapping Type

(Depracated in 6.0)

#### Field datatype

Each field has a data type which can be:

- a simple type like text, keyword, date, long, double, boolean or ip.
- a type which supports the hierarchical nature of JSON such as object or nested.
- or a specialised type like geo_point, geo_shape, or completion.

It is often useful to index the same field in different ways for different purposes. For instance, a string field could be indexed as a text field for full-text search, and as a keyword field for sorting or aggregations. Alternatively, you could index a string field with the standard analyzer, the english analyzer, and the french analyzer.

**Settings to prevent mapping explosion**:
- Not too many
- Not too _deep_ (nested)

### Dynamic Mapping

You don't have to define before being used.