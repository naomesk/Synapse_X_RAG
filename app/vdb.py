from pymilvus import FieldSchema, CollectionSchema, DataType, Collection, connections, utility

# connections.connect(
#     alias="default",
#     uri="./rag_vdb.db"
# )

connections.connect("default", host="localhost", port="19530")

dim = 1024  # embedding dimension (IMPORTANT: must match your model)

fields = [
    FieldSchema(
        name="chunk_id",
        dtype=DataType.INT64,
        is_primary=True,
        auto_id=True
    ),
    FieldSchema(
        name="embedding_vector",
        dtype=DataType.FLOAT_VECTOR,
        dim=dim
    ),
    FieldSchema(
        name="document_id",
        dtype=DataType.VARCHAR,
        max_length=64
    ),
    FieldSchema(
        name="chunk_index",
        dtype=DataType.INT64,
        max_length=64
    )
]

schema = CollectionSchema(
    fields=fields,
    description="Document chunks with embeddings", 
    enable_dynamic_field=False
)

collection_name = "document_chunks"

if not utility.has_collection(collection_name):
    collection = Collection(name=collection_name, schema=schema)
else:
    collection = Collection(name=collection_name)

index_params = {
    "metric_type": "IP",
    "index_type": "HNSW",
    "params": {
        "M": 16, 
        "efConstruction": 200
    }
}
if not collection.has_index():
    collection.create_index(
        field_name="embedding_vector", 
        index_params=index_params
    )

collection.load()
print(utility.list_collections())
collection = Collection("document_chunks")
print(collection.schema)
print(collection.num_entities)