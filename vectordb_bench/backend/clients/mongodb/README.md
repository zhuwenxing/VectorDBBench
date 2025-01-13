How to Index Fields for Vector Search
You can use the vectorSearch type to index fields for running $vectorSearch queries. You can define the index for the vector embeddings that you want to query and the boolean, date, objectId, numeric, string, or UUID values that you want to use to pre-filter your data. Filtering your data is useful to narrow the scope of your semantic search and ensure that certain vector embeddings are not considered for comparison, such as in a multi-tenant environment.

You can use the Atlas UI, Atlas Administration API, Atlas CLI, mongosh, or a supported MongoDB Driver to create your Atlas Vector Search index.

Note
You can't use the deprecated knnBeta operator to query fields indexed using the vectorSearch type index definition.

Considerations
In a vectorSearch type index definition, you can index arrays with only a single element. You can't index fields inside arrays of documents or fields inside arrays of objects. You can index fields inside documents using the dot notation.

Before indexing your embeddings, we recommend converting your embeddings to BSON BinData vector subtype float32, int1, or int8 vectors for efficient storage in your Atlas cluster. To learn more, see how to convert your embeddings to BSON vectors.

Note
Atlas Vector Search support for the following is available as a Preview feature:

Ingestion of BSON BinData vector subtype int1.

Automatic scalar quantization.

Automatic binary quantization.

When you use Atlas Vector Search indexes, you might experience elevated resource consumption on an idle node for your Atlas cluster. This is due to the underlying mongot process, which performs various essential operations for Atlas Vector Search. The CPU utilization on an idle node can vary depending on the number, complexity, and size of the indexes.

Supported Clients
You can create and manage Atlas Vector Search indexes through the Atlas UI, mongosh, Atlas CLI, Atlas Administration API, and the following MongoDB Drivers:

MongoDB Driver
Version
C

1.28.0 or higher

C++

3.11.0 or higher

C#

3.1.0 or higher

Go

1.16.0 or higher

Java

5.2.0 or higher

Kotlin

5.2.0 or higher

Node

6.6.0 or higher

PHP

1.20.0 or higher

Python

4.7 or higher

Rust

3.1.0 or higher

Scala

5.2.0 or higher

Syntax
The following syntax defines the vectorSearch index type:

{
  "fields":[
    {
      "type": "vector",
      "path": "<field-to-index>",
      "numDimensions": <number-of-dimensions>,
      "similarity": "euclidean | cosine | dotProduct",
      "quantization": "none | scalar | binary"
    },
    {
      "type": "filter",
      "path": "<field-to-index>"
    },
    ...
  ]
}

Atlas Vector Search Index Fields
The Atlas Vector Search index definition takes the following fields:

Option
Type
Necessity
Purpose
fields

array of documents

Required

Vector and filter fields to index, one per document. At least one document must contain the field definition for the vector field. You can optionally also index boolean, date, number, objectId, string, and UUID fields, one per document, for pre-filtering the data.

fields.type

string

Required

Field type to use to index fields for $vectorSearch. You can specify one of the following values:

vector - for fields that contain vector embeddings.

filter - for fields that contain boolean, date, objectId, numeric, string, or UUID values.

fields.path

string

Required

Name of the field to index. For nested fields, use dot notation to specify path to embedded fields.

You cannot index field names with two consecutive dots or field names ending with dots. For example, Atlas Vector Search doesn't support indexing the following field names: foo..bar or foo_bar..

fields.numDimensions

int

Required

Number of vector dimensions that Atlas Vector Search enforces at index-time and query-time. You must specify a value less than or equal to 4096. For indexing BinData or quantized vectors, value must be one of the following:

1 to 4096 for int8 vectors for ingestion.

Multiple of 8 for int1 vectors for ingestion.

1 to 4096 for binData(float32) and array(float32) vectors for automatic scalar quantization.

Multiple of 8 for binData(float32) and array(float32) vectors for automatic binary quantization.

You can set this field only for vector type fields.

fields.similarity

string

Required

Vector similarity function to use to search for top K-nearest neighbors. You can set this field only for vector type fields. Value can be one of the following:

euclidean - measures the distance between ends of vectors.

cosine - measures similarity based on the angle between vectors.

dotProduct - measures similarity like cosine, but takes into account the magnitude of the vector.

To learn more, see About the Similarity Functions.

fields.quantization

string

Optional

Type of automatic vector quantization for your vectors. You can specify the type of quantization to apply on your vectors. Use this setting only if your embeddings are float or double vectors. Value can be one of the following:

none - Indicates no automatic quantization for the vector embeddings. Use this setting if you have pre-quantized vectors for ingestion. If omitted, this is the default value.

scalar - Indicates scalar quantization, which transforms values to 1 byte integers.

binary - Indicates binary quantization, which transforms values to a single bit. To use this quantization, numDimensions must be a multiple of 8.

If precision is critical, select none or scalar instead of binary.

To learn more, see Vector Quantization.

About the vector Type
Your index definition's vector field must contain an array of numbers of one of the following types:

BSON double

BSON BinData vector subtype float32

BSON BinData vector subtype int1

BSON BinData vector subtype int8

Note
To learn more about generating BSON BinData vector subtype float32 or vector subtype int1 or int8 vectors for your data, see How to Ingest Pre-Quantized Vectors.

Atlas Vector Search support for the following is available as a Preview feature:

Ingestion of BSON BinData vector subtype int1.

Automatic scalar quantization.

Automatic binary quantization.

You must index the vector field as the vector type inside the fields array.

The following syntax defines the vector field type:

{
  "fields":[
    {
      "type": "vector",
      "path": <field-to-index>,
      "numDimensions": <number-of-dimensions>,
      "similarity": "euclidean | cosine | dotProduct",
      "quantization": "none | scalar | binary"
    },
    ...
  ]
}

About the Similarity Functions
Atlas Vector Search supports the following similarity functions:

euclidean - measures the distance between ends of vectors. This value allows you to measure similarity based on varying dimensions. To learn more, see Euclidean.

cosine - measures similarity based on the angle between vectors. This value allows you to measure similarity that isn't scaled by magnitude. You can't use zero magnitude vectors with cosine. To measure cosine similarity, we recommend that you normalize your vectors and use dotProduct instead.

dotProduct - measures similarity like cosine, but takes into account the magnitude of the vector. If you normalize the magnitude, cosine and dotProduct are almost identical in measuring similarity.

To use dotProduct, you must normalize the vector to unit length at index-time and query-time.

The following table shows the similarity functions for the various types:

Vector Embeddings Type
euclidean
consine
dotProduct
binData(int1) 

√

binData(int8) 

√

√

√

binData(float32) 

√

√

√

array(float32) 

√

√

√

 For vector ingestion.

 For automatic scalar or binary quantization.

For best performance, check your embedding model to determine which similarity function aligns with your embedding model's training process. If you don't have any guidance, start with dotProduct. Setting fields.similarity to the dotProduct value allows you to efficiently measure similarity based on both angle and magnitude. dotProduct consumes less computational resources than cosine and is efficient when vectors are of unit length. However, if your vectors aren't normalized, evaluate the similarity scores in the results of a sample query for euclidean distance and cosine similarity to determine which corresponds to reasonable results.

About the filter Type
You can optionally index boolean, date, number, objectId, string, and UUID fields to pre-filter your data. Filtering your data is useful to narrow the scope of your semantic search and ensure that not all vectors are considered for comparison. It reduces the number of documents against which to run similarity comparisons, which can decrease query latency and increase the accuracy of search results.

You must index the fields that you want to filter by using the filter type inside the fields array.

The following syntax defines the filter field type:

{
  "fields":[
    {
      "type": "vector",
      ...
    },
    {
      "type": "filter",
      "path": "<field-to-index>"
    },
    ...
  ]
}

Note
Pre-filtering your data doesn't affect the score that Atlas Vector Search returns using $vectorSearchScore for $vectorSearch queries.

Create an Atlas Vector Search Index
An Atlas Search index is a data structure that categorizes data in an easily searchable format. It is a mapping between terms and the documents that contain those terms. Atlas Search indexes enable faster retrieval of documents using certain identifiers. You must configure an Atlas Search index to query data in your Atlas cluster using Atlas Search.

You can create an Atlas Search index on a single field or on multiple fields. We recommend that you index the fields that you regularly use to sort or filter your data in order to quickly retrieve the documents that contain the relevant data at query-time.

You can create an Atlas Vector Search index for all collections that contain vector embeddings less than or equal to 4096 dimensions in length for any kind of data along with other data on your Atlas cluster through the Atlas UI, Atlas Administration API, Atlas CLI, mongosh, or a supported MongoDB Driver.

Prerequisites
To create an Atlas Vector Search index, you must have an Atlas cluster with the following prerequisites:

MongoDB version 6.0.11, 7.0.2, or higher

A collection for which to create the Atlas Vector Search index

Note
You can use the mongosh command or driver helper methods to create Atlas Search indexes on all Atlas cluster tiers. For a list of supported driver versions, see Supported Clients.

Required Access
You need the Project Data Access Admin or higher role to create and manage Atlas Vector Search indexes.

Index Limitations
You cannot create more than:

3 indexes on M0 clusters.

5 indexes on M2 clusters.

10 indexes on M5 clusters.

We recommend that you create no more than 2,500 search indexes on a single M10+ cluster.

Procedure
➤ Use the Select your language drop-down menu to select the client you want to use to create your index.

Note
The procedure includes index definition examples for the embedded_movies collection in the sample_mflix database. If you load the sample data on your cluster and create the example Atlas Search indexes for this collection, you can run the sample $vectorSearch queries against this collection. To learn more about the sample queries that you can run, see $vectorSearch Examples.

To create an Atlas Vector Search index for a collection using the PyMongo driver v4.7 or later, perform the following steps:

1
Create a .py file and define the index in the file.

Single Index

Multiple Indexes
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
# Connect to your Atlas deployment
uri = "<connectionString>"
client = MongoClient(uri)
# Access your database and collection
database = client["<databaseName>"]
collection = database["<collectionName>"]
# Create your index model, then create the search index
search_index_model = SearchIndexModel(
  definition={
    "fields": [
      {
        "type": "vector",
        "numDimensions": <numberofDimensions>,
        "path": "<fieldToIndex>",
        "similarity": "euclidean | cosine | dotProduct"
      },
      {
        "type": "filter",
        "path": "<fieldToIndex>"
      },
      ...
    ]
  },
  name="<indexName>",
  type="vectorSearch",
)
result = collection.create_search_index(model=search_index_model)
print("New search index named " + result + " is building.")
# Wait for initial sync to complete
print("Polling to check if the index is ready. This may take up to a minute.")
predicate=None
if predicate is None:
  predicate = lambda index: index.get("queryable") is True
while True:
  indices = list(collection.list_search_indexes(result))
  if len(indices) and predicate(indices[0]):
    break
  time.sleep(5)
print(result + " is ready for querying.")
client.close()


To learn more, see the create_search_index() method.

Example
Create a file named vector-index.py.

2
Replace the following values and save the file.
<connectionString>

Atlas connection string. To learn more, see Connect via Drivers.

<databaseName>

Database that contains the collection for which you want to create the index.

<collectionName>

Collection for which you want to create the index.

<indexName>

Name of your index. If you omit the index name, Atlas Search names the index vector_index.

<numberOfDimensions>

Number of vector dimensions that Atlas Vector Search enforces at index-time and query-time.

<fieldToIndex>

Vector and filter fields to index.

Example
Copy and paste the following into the vector-index.py and replace the <connectionString> placeholder value. The following index definition indexes the plot_embedding field as the vector type and the genres and year fields as the filter type in an Atlas Vector Search index. The plot_embedding field contains embeddings created using OpenAI's text-embedding-ada-002 embeddings model. The index definition specifies 1536 vector dimensions and measures similarity using dotProduct function.


Basic Example

Filter Example
The following index definition indexes only the vector embeddings field (plot_embedding) for performing vector search.

from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
import time
# Connect to your Atlas deployment
uri = "<connectionString>"
client = MongoClient(uri)
# Access your database and collection
database = client["sample_mflix"]
collection = database["embedded_movies"]
# Create your index model, then create the search index
search_index_model = SearchIndexModel(
  definition={
    "fields": [
      {
        "type": "vector",
        "path": "plot_embedding",
        "numDimensions": 1536,
        "similarity": "dotProduct"
      }
    ]
  },
  name="vector_index",
  type="vectorSearch",
)
result = collection.create_search_index(model=search_index_model)
print("New search index named " + result + " is building.")
# Wait for initial sync to complete
print("Polling to check if the index is ready. This may take up to a minute.")
predicate=None
if predicate is None:
  predicate = lambda index: index.get("queryable") is True
while True:
  indices = list(collection.list_search_indexes(name))
  if len(indices) and predicate(indices[0]):
    break
  time.sleep(5)
print(result + " is ready for querying.")
client.close()


3
Run the following command to create the index.
python <file-name>.py


Example
python vector-index.py


View an Atlas Vector Search Index
You can view Atlas Vector Search indexes for all collections from the Atlas UI, Atlas Administration API, Atlas CLI, mongosh, or a supported MongoDB Driver.

Required Access
You need the Project Search Index Editor or higher role to view Atlas Vector Search indexes.

Note
You can use the mongosh command or driver helper methods to retrieve Atlas Search indexes on all Atlas cluster tiers. For a list of supported driver versions, see Supported Clients.

Procedure
➤ Use the Select your language drop-down menu to set the language of the example in this section.

To view Atlas Vector Search indexes for a collection using PyMongo driver v4.7 or later, perform the following steps:

1
Create a .py file and use the list_search_indexes() method to retrieve the indexes for the collection.
from pymongo.mongo_client import MongoClient
# Connect to your Atlas deployment
uri = "<connectionString>"
client = MongoClient(uri)
# Access your database and collection
database = client["<databaseName>"]
collection = database["<collectionName>"]
# Get a list of the collection's search indexes and print them
cursor = collection.list_search_indexes()
for index in cursor:
    print(index)


To learn more, see the list_search_indexes() method.

2
Replace the following values and save the file.
<connectionString>

Your Atlas connection string. To learn more, see Connect via Drivers.

<databaseName>

The name of the database that contains the collection.

<collectionName>

The name of the collection.

3
Run the following command to retrieve the indexes.
python <file-name>.py


Edit an Atlas Vector Search Index
You can change the index definition of an existing Atlas Vector Search index from the Atlas UI, Atlas Administration API, Atlas CLI, mongosh, or a supported MongoDB Driver. You can't rename an index or change the index type. If you need to change an index name or type, you must create a new index and delete the old one.

Important
After you edit an index, Atlas Vector Search rebuilds it. While the index rebuilds, you can continue to run vector search queries by using the old index definition. When the index finishes rebuilding, the old index is automatically replaced. This process follows the same process as standard Atlas Search indexes.

To learn more, see Creating and Updating an Atlas Search Index.

Required Access
You must have the Project Search Index Editor or higher role to edit an Atlas Vector Search index.

Note
You can use the mongosh command or driver helper methods to edit Atlas Search indexes on all Atlas cluster tiers. For a list of supported driver versions, see Supported Clients.

Procedure
➤ Use the Select your language drop-down menu to select the client you want to use to edit your index.

To update an Atlas Vector Search index for a collection using the PyMongo driver v4.7 or later, perform the following steps:

1
Create the .py file and define the index changes in the file.
from pymongo.mongo_client import MongoClient
# Connect to your Atlas deployment
uri = "<connectionString>"
client = MongoClient(uri)
# Access your database and collection
database = client["<databaseName>"]
collection = database["<collectionName>"]
definition = {
  "fields": [
    {
      "type": "vector",
      "numDimensions": <numberofDimensions>,
      "path": "<fieldToIndex>",
      "similarity": "euclidean | cosine | dotProduct"
    },
    {
      "type": "filter",
      "path": "<fieldToIndex>"
    },
    ...
  ]
}
    
# Update your search index
collection.update_search_index("<indexName>", definition)


To learn more, see the update_search_index() method.

2
Replace the following values and save the file.
<connectionString>

Atlas connection string. To learn more, see Connect via Drivers.

<databaseName>

Database that contains the collection for which you want to create the index.

<collectionName>

Collection for which you want to create the index.

<indexName>

Bame of your index. If you omit the index name, Atlas Search names the index vector_index.

<numberOfDimensions>

Number of vector dimensions that Atlas Vector Search enforces at index-time and query-time.

<fieldToIndex>

Vector and filter fields to index.

3
Run the following command to update the index.
python <file-name>.py


Delete an Atlas Vector Search Index
You can delete an Atlas Vector Search index at any time from the Atlas UI, Atlas Administration API, Atlas CLI, mongosh, or a supported MongoDB Driver.

Required Access
You must have the Project Search Index Editor or higher role to delete an Atlas Vector Search index.

Note
You can use the mongosh command or driver helper methods to delete Atlas Search indexes on all Atlas cluster tiers. For a list of supported driver versions, see Supported Clients.

Procedure
➤ Use the Select your language drop-down menu to select the client you want to use to delete your index.

To delete an Atlas Vector Search index for a collection using PyMongo driver v4.7 or later, perform the following steps:

1
Create the .py file and use the drop_search_index() method to delete the index.
from pymongo.mongo_client import MongoClient
# Connect to your Atlas deployment
uri = "<connectionString>"
client = MongoClient(uri)
# Access your database and collection
database = client["<databaseName>"]
collection = database["<collectionName>"]
# Delete your search index
collection.drop_search_index("<indexName>")


To learn more, see the drop_search_index() method.

2
Replace the following values and save the file.
<connectionString>

Your Atlas connection string. To learn more, see Connect via Drivers.

<databaseName>

The name of the database that contains the collection.

<collectionName>

The name of the collection.

<indexName>

The name of the index to delete.

3
Run the following command to delete the index.
python <file-name>.py


Index Status
When you create the Atlas Vector Search index, the Status column shows the current state of the index on the primary node of the cluster. Click the View status details link below the status to view the state of the index on all the nodes of the cluster.

When the Status column reads Active, the index is ready to use. In other states, queries against the index may return incomplete results.

Status
Description
Not Started

Atlas has not yet started building the index.

Initial Sync

Atlas is building the index or re-building the index after an edit. When the index is in this state:

For a new index, Atlas Vector Search doesn't serve queries until the index build is complete.

For an existing index, you can continue to use the old index for existing and new queries until the index rebuild is complete.

Active

Index is ready to use.

Recovering

Replication encountered an error. This state commonly occurs when the current replication point is no longer available on the mongod oplog. You can still query the existing index until it updates and its status changes to Active. Use the error in the View status details modal window to troubleshoot the issue. To learn more, see Fix Atlas Search Issues.

Failed

Atlas could not build the index. Use the error in the View status details modal window to troubleshoot the issue. To learn more, see Fix Atlas Search Issues.

Delete in Progress

Atlas is deleting the index from the cluster nodes.

While Atlas builds the index and after the build completes, the Documents column shows the percentage and number of documents indexed. The column also shows the total number of documents in the collection.



Run Vector Search Queries
Atlas Vector Search queries take the form of an aggregation pipeline stage. For the $vectorSearch queries, Atlas Vector Search returns the results of your semantic search.

Note
Definition
The $vectorSearch stage performs an ANN or ENN search on a vector in the specified field.

ANN Search
For ANN search, Atlas Vector Search finds vector embeddings in your data that are closest to the vector embedding in your query based on their proximity in multi-dimensional space and based on the number of neighbors that it considers. It uses the Hierarchical Navigable Small Worlds algorithm and finds the vector embeddings most similar to the vector embedding in your query without scanning every vector. Therefore, ANN search is ideal for querying large datasets without significant filtering.

ENN Search
For ENN search, Atlas Vector Search exhaustively searches all the indexed vector embeddings by calculating the distance between all the embeddings and finds the exact nearest neighbor for the vector embedding in your query. This is computationally intensive and might negatively impact query latency. Therefore, we recommend ENN searches for the following use-cases:

You want to determine the recall and accuracy of your ANN query using the ideal, exact results for the ENN query.

You want to query less than 10000 documents without having to tune the number of nearest neighbors to consider.

Your want to include selective pre-filters in your query against collections where less than 5% of your data meets the given pre-filter.

Syntax
The field that you want to search must be indexed as Atlas Vector Search vector type inside a vectorSearch index type.

$vectorSearch
A $vectorSearch pipeline has the following prototype form:

{
  "$vectorSearch": {
    "exact": true | false,
    "filter": {<filter-specification>},
    "index": "<index-name>",
    "limit": <number-of-results>,
    "numCandidates": <number-of-candidates>,
    "path": "<field-to-search>",
    "queryVector": [<array-of-numbers>]
  }
}

Fields
The $vectorSearch stage takes a document with the following fields:

Field
Type
Necessity
Description
exact

boolean

Optional

This is required if numCandidates is omitted.

Flag that specifies whether to run ENN or ANN search. Value can be one of the following:

false - to run ANN search

true - to run ENN search

If omitted, defaults to false.

Atlas Vector Search supports ANN search on clusters running MongoDB v6.0.11, v7.0.2, or later and ENN search on clusters running MongoDB v6.0.16, v7.0.10, v7.3.2, or later.

filter

document

Optional

Any MQL match expression that compares an indexed field with a boolean, date, objectId, number (not decimals), string, or UUID to use as a pre-filter. To learn which query and aggregation pipeline operators Atlas Vector Search supports in your filter, see Atlas Vector Search Pre-Filter.

index

string

Required

Name of the Atlas Vector Search index to use.

Atlas Vector Search doesn't return results if you misspell the index name or if the specified index doesn't already exist on the cluster.

limit

number

Required

Number (of type int only) of documents to return in the results. This value can't exceed the value of numCandidates if you specify numCandidates.

numCandidates

number

Optional

This field is required if exact is false or omitted.

Number of nearest neighbors to use during the search. Value must be less than or equal to (<=) 10000. You can't specify a number less than the number of documents to return (limit).

We recommend that you specify a number higher than the number of documents to return (limit) to increase accuracy although this might impact latency. For example, we recommend a ratio of ten to twenty nearest neighbors for a limit of only one document. This overrequest pattern is the recommended way to trade off latency and recall in your ANN searches, and we recommend tuning this on your specific dataset.

path

string

Required

Indexed vector type field to search. To learn more, see Path Construction.

queryVector

array of numbers

Required

Array of numbers of the BSON double, BSON BinData vector subtype float32, or BSON BinData vector subtype int1 or int8 type that represent the query vector. The number type must match the indexed field value type. Otherwise, Atlas Vector Search doesn't return any results or errors.

To learn more about generating BSON BinData vector subtype float32 or vector subtype int1 or int8 vectors for your query, see How to Ingest Pre-Quantized Vectors.

The array size must match the number of vector dimensions specified in the index definition for the field.

You must embed your query with the same model that you used to embed the data.

Behavior
$vectorSearch must be the first stage of any pipeline where it appears.

Atlas Vector Search Index
You must index the fields to search using the $vectorSearch stage inside a vectorSearch type index definition. You can index the following types of fields in an Atlas Vector Search vectorSearch type index definition:

Fields that contain vector embeddings as vector type.

Fields that contain boolean, date, objectId, numeric, string, and UUID values as filter type to enable vector search on pre-filtered data.

To learn more about these Atlas Vector Search field types, see How to Index Fields for Vector Search.

Atlas Vector Search Score
Atlas Vector Search assigns a score, in a fixed range from 0 to 1 (where 0 indicates low similarity and 1 indicates high similarity), to every document that it returns. For cosine and dotProduct similarities, Atlas Vector Search normalizes the score to ensure that the score is not negative.

For cosine, Atlas Vector Search uses the following algorithm to normalize the score:

score = (1 + cosine(v1,v2)) / 2
For dotProduct, Atlas Vector Search uses the following algorithm to normalize the score:

score = (1 + dotProduct(v1,v2)) / 2
These algorithms show that Atlas Vector Search normalizes the score by considering the similarity score of the document vector (v1) and the query vector (v2), which has the range [-1, 1]. Atlas Vector Search adds 1 to the similarity score to normalize the score to a range [0, 2] and then divides by 2 to ensure a value between 0 and 1.

For euclidean similarity, Atlas Vector Search uses the following algorithm to normalize the score to ensure a value between 0 and 1:

score = 1 / (1 + euclidean(v1,v2))
The preceding algorithm shows that Atlas Vector Search normalizes the score by calculating the euclidean distance, which is the distance between the document vector (v1) and the query vector (v2), which has the range [0, ∞]. Atlas Vector Search then transforms the distance to a similarity score by adding 1 to the distance and then divides 1 by the similarity score to ensure a value between 0 and 1.

The score assigned to a returned document is part of the document's metadata. To include each returned document's score along with the result set, use a $project stage in your aggregation pipeline.

To retrieve the score of your Atlas Vector Search query results, use vectorSearchScore as the value in the $meta expression. That is, after the $vectorSearch stage, in the $project stage, the score field takes the $meta expression. The expression requires the vectorSearchScore value to return the score of documents for the vector search.

Example
db.<collection>.aggregate([
  {
    "$vectorSearch": {
      <query-syntax>
    }
  },
  {
    "$project": {
      "<field-to-include>": 1,
      "<field-to-exclude>": 0,
      "score": { "$meta": "vectorSearchScore" }
    }
  }
])
Note
Pre-filtering your data doesn't affect the score that Atlas Vector Search returns using $vectorSearchScore for $vectorSearch queries.

Atlas Vector Search Pre-Filter
The $vectorSearch filter option matches only BSON boolean, date, objectId, numeric, string, and UUID values. You must index the fields that you want to filter your data by as the filter type in a vectorSearch type index definition. Filtering your data is useful to narrow the scope of your semantic search and ensure that not all vectors are considered for comparison.

Atlas Vector Search supports the $vectorSearch filter option for the following MQL match expressions:

$gt

$lt

$gte

$lte

$eq

$ne

$in

$nin

$nor

$not

$and

$or

The $vectorSearch filter option supports only the following aggregation pipeline operators:

$and

$or

Note
The $vectorSearch filter option doesn't support other query operators, aggregation pipeline operators, or Atlas Search operators.

Considerations
Atlas Vector Search supports the short form of $eq. In the short form, you don't need to specify $eq in the query.

Example
For example, consider the following filter with $eq:

"filter": { "_id": { "$eq": ObjectId("5a9427648b0beebeb69537a5") }
You can run the preceding query using the short form of $eq in the following way:

"filter": { "_id": ObjectId("5a9427648b0beebeb69537a5") }
You can also specify an array of filters in a single query by using the $and operator.

Example
For example, consider the following pre-filter for documents with a genres field equal to Action and a year field with the value 1999, 2000, or 2001:

"filter": {
  "$and": [
    { "genres": "Action" },
    { "year": { "$in": [ 1999, 2000, 2001 ] } }
  ]
}
Limitations
$vectorSearch is supported only on Atlas clusters running the following MongoDB versions:

v6.0.11

v7.0.2 and later (including RCs).

$vectorSearch can't be used in view definition and the following pipeline stages:

$lookup sub-pipeline 

$unionWith sub-pipeline 

$facet pipeline stage

 You can pass the results of $vectorSearch to this stage.

Supported Clients
You can run $vectorSearch queries by using the Atlas UI, mongosh, and any MongoDB driver.

You can also use Atlas Vector Search with local Atlas deployments that you create with the Atlas CLI. To learn more, see Create a Local Atlas Deployment.

Parallel Query Execution Across Segments
We recommend dedicated Search Nodes to isolate vector search query processing. You might see improved query performance on the dedicated Search Nodes. Note that the high-CPU systems might provide more performance improvement. When Atlas Vector Search runs on search nodes, Atlas Vector Search parallelizes query execution across segments of data.

Parallelization of query processing improves the response time in many cases, such as queries on large datasets. Using intra-query parallelism during Atlas Vector Search query processing utilizes more resources, but improves latency for each individual query.

Note
Atlas Vector Search doesn't guarantee that each query will run concurrently. For example, when too many concurrent queries are queued, Atlas Vector Search might fall back to single-threaded execution.

You might see inconsistent results for the same successive queries. To mitigate this, increase the value of numCandidates in your $vectorSearch queries.

Examples
The following queries search the sample sample_mflix.embedded_movies collection using the $vectorSearch stage. The queries search the plot_embedding field, which contains embeddings created using OpenAI's text-embedding-ada-002 embeddings model. If you added the sample collection to your Atlas cluster and created the sample indexes for the collection, you can run the following queries against the collection.

Note
Pasting the queryVector from the sample code into your terminal might take a while depending on your machine.

➤ Use the Select your language drop-down menu to set the language of the examples in this page.



Atlas Vector Search queries take the form of an aggregation pipeline stage. For the $vectorSearch queries, Atlas Vector Search returns the results of your semantic search.

Note
Definition
The $vectorSearch stage performs an ANN or ENN search on a vector in the specified field.

ANN Search
For ANN search, Atlas Vector Search finds vector embeddings in your data that are closest to the vector embedding in your query based on their proximity in multi-dimensional space and based on the number of neighbors that it considers. It uses the Hierarchical Navigable Small Worlds algorithm and finds the vector embeddings most similar to the vector embedding in your query without scanning every vector. Therefore, ANN search is ideal for querying large datasets without significant filtering.

ENN Search
For ENN search, Atlas Vector Search exhaustively searches all the indexed vector embeddings by calculating the distance between all the embeddings and finds the exact nearest neighbor for the vector embedding in your query. This is computationally intensive and might negatively impact query latency. Therefore, we recommend ENN searches for the following use-cases:

You want to determine the recall and accuracy of your ANN query using the ideal, exact results for the ENN query.

You want to query less than 10000 documents without having to tune the number of nearest neighbors to consider.

Your want to include selective pre-filters in your query against collections where less than 5% of your data meets the given pre-filter.

Syntax
The field that you want to search must be indexed as Atlas Vector Search vector type inside a vectorSearch index type.

$vectorSearch
A $vectorSearch pipeline has the following prototype form:

{
  "$vectorSearch": {
    "exact": true | false,
    "filter": {<filter-specification>},
    "index": "<index-name>",
    "limit": <number-of-results>,
    "numCandidates": <number-of-candidates>,
    "path": "<field-to-search>",
    "queryVector": [<array-of-numbers>]
  }
}

Fields
The $vectorSearch stage takes a document with the following fields:

Field
Type
Necessity
Description
exact

boolean

Optional

This is required if numCandidates is omitted.

Flag that specifies whether to run ENN or ANN search. Value can be one of the following:

false - to run ANN search

true - to run ENN search

If omitted, defaults to false.

Atlas Vector Search supports ANN search on clusters running MongoDB v6.0.11, v7.0.2, or later and ENN search on clusters running MongoDB v6.0.16, v7.0.10, v7.3.2, or later.

filter

document

Optional

Any MQL match expression that compares an indexed field with a boolean, date, objectId, number (not decimals), string, or UUID to use as a pre-filter. To learn which query and aggregation pipeline operators Atlas Vector Search supports in your filter, see Atlas Vector Search Pre-Filter.

index

string

Required

Name of the Atlas Vector Search index to use.

Atlas Vector Search doesn't return results if you misspell the index name or if the specified index doesn't already exist on the cluster.

limit

number

Required

Number (of type int only) of documents to return in the results. This value can't exceed the value of numCandidates if you specify numCandidates.

numCandidates

number

Optional

This field is required if exact is false or omitted.

Number of nearest neighbors to use during the search. Value must be less than or equal to (<=) 10000. You can't specify a number less than the number of documents to return (limit).

We recommend that you specify a number higher than the number of documents to return (limit) to increase accuracy although this might impact latency. For example, we recommend a ratio of ten to twenty nearest neighbors for a limit of only one document. This overrequest pattern is the recommended way to trade off latency and recall in your ANN searches, and we recommend tuning this on your specific dataset.

path

string

Required

Indexed vector type field to search. To learn more, see Path Construction.

queryVector

array of numbers

Required

Array of numbers of the BSON double, BSON BinData vector subtype float32, or BSON BinData vector subtype int1 or int8 type that represent the query vector. The number type must match the indexed field value type. Otherwise, Atlas Vector Search doesn't return any results or errors.

To learn more about generating BSON BinData vector subtype float32 or vector subtype int1 or int8 vectors for your query, see How to Ingest Pre-Quantized Vectors.

The array size must match the number of vector dimensions specified in the index definition for the field.

You must embed your query with the same model that you used to embed the data.

Behavior
$vectorSearch must be the first stage of any pipeline where it appears.

Atlas Vector Search Index
You must index the fields to search using the $vectorSearch stage inside a vectorSearch type index definition. You can index the following types of fields in an Atlas Vector Search vectorSearch type index definition:

Fields that contain vector embeddings as vector type.

Fields that contain boolean, date, objectId, numeric, string, and UUID values as filter type to enable vector search on pre-filtered data.

To learn more about these Atlas Vector Search field types, see How to Index Fields for Vector Search.

Atlas Vector Search Score
Atlas Vector Search assigns a score, in a fixed range from 0 to 1 (where 0 indicates low similarity and 1 indicates high similarity), to every document that it returns. For cosine and dotProduct similarities, Atlas Vector Search normalizes the score to ensure that the score is not negative.

For cosine, Atlas Vector Search uses the following algorithm to normalize the score:

score = (1 + cosine(v1,v2)) / 2
For dotProduct, Atlas Vector Search uses the following algorithm to normalize the score:

score = (1 + dotProduct(v1,v2)) / 2
These algorithms show that Atlas Vector Search normalizes the score by considering the similarity score of the document vector (v1) and the query vector (v2), which has the range [-1, 1]. Atlas Vector Search adds 1 to the similarity score to normalize the score to a range [0, 2] and then divides by 2 to ensure a value between 0 and 1.

For euclidean similarity, Atlas Vector Search uses the following algorithm to normalize the score to ensure a value between 0 and 1:

score = 1 / (1 + euclidean(v1,v2))
The preceding algorithm shows that Atlas Vector Search normalizes the score by calculating the euclidean distance, which is the distance between the document vector (v1) and the query vector (v2), which has the range [0, ∞]. Atlas Vector Search then transforms the distance to a similarity score by adding 1 to the distance and then divides 1 by the similarity score to ensure a value between 0 and 1.

The score assigned to a returned document is part of the document's metadata. To include each returned document's score along with the result set, use a $project stage in your aggregation pipeline.

To retrieve the score of your Atlas Vector Search query results, use vectorSearchScore as the value in the $meta expression. That is, after the $vectorSearch stage, in the $project stage, the score field takes the $meta expression. The expression requires the vectorSearchScore value to return the score of documents for the vector search.

Example
db.<collection>.aggregate([
  {
    "$vectorSearch": {
      <query-syntax>
    }
  },
  {
    "$project": {
      "<field-to-include>": 1,
      "<field-to-exclude>": 0,
      "score": { "$meta": "vectorSearchScore" }
    }
  }
])
Note
Pre-filtering your data doesn't affect the score that Atlas Vector Search returns using $vectorSearchScore for $vectorSearch queries.

Atlas Vector Search Pre-Filter
The $vectorSearch filter option matches only BSON boolean, date, objectId, numeric, string, and UUID values. You must index the fields that you want to filter your data by as the filter type in a vectorSearch type index definition. Filtering your data is useful to narrow the scope of your semantic search and ensure that not all vectors are considered for comparison.

Atlas Vector Search supports the $vectorSearch filter option for the following MQL match expressions:

$gt

$lt

$gte

$lte

$eq

$ne

$in

$nin

$nor

$not

$and

$or

The $vectorSearch filter option supports only the following aggregation pipeline operators:

$and

$or

Note
The $vectorSearch filter option doesn't support other query operators, aggregation pipeline operators, or Atlas Search operators.

Considerations
Atlas Vector Search supports the short form of $eq. In the short form, you don't need to specify $eq in the query.

Example
For example, consider the following filter with $eq:

"filter": { "_id": { "$eq": ObjectId("5a9427648b0beebeb69537a5") }
You can run the preceding query using the short form of $eq in the following way:

"filter": { "_id": ObjectId("5a9427648b0beebeb69537a5") }
You can also specify an array of filters in a single query by using the $and operator.

Example
For example, consider the following pre-filter for documents with a genres field equal to Action and a year field with the value 1999, 2000, or 2001:

"filter": {
  "$and": [
    { "genres": "Action" },
    { "year": { "$in": [ 1999, 2000, 2001 ] } }
  ]
}
Limitations
$vectorSearch is supported only on Atlas clusters running the following MongoDB versions:

v6.0.11

v7.0.2 and later (including RCs).

$vectorSearch can't be used in view definition and the following pipeline stages:

$lookup sub-pipeline 

$unionWith sub-pipeline 

$facet pipeline stage

