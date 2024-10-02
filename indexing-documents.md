# Indexing Box documents

After generating sample data in your Box account, you can now index the documents in a Box folder using LlamaIndex and ChromaDB.

We'll use the LlamaIndex Box reader to access the files, and ChromaDB to build the index.

## LlamaIndex Box reader

The LlamaIndex Box reader is a Python class that reads documents from a Box folder. It uses the Box Python SDK to access the files and fetch their content.

In the example we broke these steps further down.

We start by searching for the documents in the Box folder:

```python
# Using BoxReader
box_reader = BoxReader(client)

leases = box_reader.search_resources(
    query="HAB-",
    ancestor_folder_ids=[conf.box_root_demo_folder],
    content_types=[SearchForContentContentTypes.NAME],
    file_extensions=["docx"],
    limit=100,
)

print(f"Leases found: {len(leases)}, reading documents from Box...")
```

Then we read the content of the documents:

```python
documents: List[Document] = []

for lease in tqdm(leases):
    document = box_reader.load_data(file_ids=[lease])
    if document:
        documents.extend(document)
```
We could have simply used the `load_data` method to read the content of the documents, but we decided to use the `tqdm` library to show a progress bar while reading the documents.

The end result is a list of LlamaIndex `Document` objects, which we can use to build the index.

## ChromaDB

Setting up ChromaDB is simple. We need to create a `ChromaVectorStore` object and a `StorageContext` object.

```python
# Setup model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# Initialize ChromaDB (Vector store)
chroma_client = chromadb.PersistentClient(path="./.chroma.db")
chroma_collection = chroma_client.get_or_create_collection("workshop_leases")

# Set up ChromaVectorStore and load in data
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
```
Notice that we are using a persistent client to store the index in a folder called `.chroma.db`. This is useful when you want to keep the index between runs, and we will use it in the next section to query the documents.

## Indexing the documents

To create the index we use the `VectorStoreIndex` class, which takes the list of documents, the storage context, and the embedding model as parameters.

```python
# Create a Chroma Index
print("\nIndexing documents...")
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=embed_model,
    show_progress=True,
)
```

## Testing the index

To test the index, we can query the indexed documents using the `as_query_engine` method.

```python
# Query Data
query_engine = index.as_query_engine()
query = "Describe the indexed documents"

response = query_engine.query(query)

print("=" * 80)
print(f"Query: {query}")
print("-" * 80)
print("Query result:")
print(response)
print("-" * 80)
print()
```

Resulting in:
```yaml
Query: Describe the indexed documents
Query result: The indexed documents include a lease agreement for habitat units on the moon. The agreement outlines details such as payment terms, permitted use of the property, compliance with outer space treaties and laws, responsibilities for maintenance, insurance requirements, termination conditions, governing laws, dispute resolution procedures, and miscellaneous clauses regarding lease transfer and force majeure events.
```

Go ahead and execute the script `src/init_chroma.py` to see the data extraction process.

Take a look at the [workshop](src/init_chroma.py) script to see how to extract data from multiple documents.