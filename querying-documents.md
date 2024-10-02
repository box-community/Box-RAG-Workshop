# Querying documents

In this section, we will query the documents we indexed in the previous section using LlamaIndex and ChromaDB.

## Loading from ChromaDB

Setting up ChromaDB is simple. We need to create a `ChromaVectorStore` object reading it from the previous exercise.
From here we read the `Collection`, create a `VectorStoreIndex` object, and load the `Index`.

```python
# Setup model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# Initialize ChromaDB (Vector store)
chroma_client = chromadb.PersistentClient(path="./.chroma.db")
chroma_collection = chroma_client.get_collection("workshop_leases")

# Set up ChromaVectorStore and load in data
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Load a Chroma Index
index = VectorStoreIndex.from_vector_store(vector_store, embed_model)
```

## Querying the documents

Now that we have the index, we can query the documents using the `as_query_engine` method, starting with a simple query.

```python
# Query Data
query_engine = index.as_query_engine()
query = "Describe the indexed documents"

response = query_engine.query(query)
print_response(query, response)
```

Finally, we prompt the user for some queries and display the results.

```python
# Example prompts
example_prompts = [
    "Describe HAB-1 type properties",
    "Describe HAB-2 type properties",
    "When does Isaac Newton lease end?",
    "What type of property does Robert Oppenheimer has?",
]

# Infinite cycle to ask the user for prompts
while True:
    # Display example prompts
    print("\nExample prompts:")
    for idx, example in enumerate(example_prompts, 1):
        print(f"{idx}. {example}")

    # Ask user for prompt or allow selection from examples
    prompt = input(
        f"\nEnter a prompt (or choose 1-{len(example_prompts)} from examples, 'q' to quit): "
    )

    if prompt == "q":
        break

    # Allow selection of example prompt if user chooses 1-5
    if prompt.isdigit() and 1 <= int(prompt) <= 5:
        prompt = example_prompts[int(prompt) - 1]

    query = prompt
    response = query_engine.query(query)
    print_response(query, response)
```
Resulting in:
```yaml
Example prompts:
1. Describe HAB-1 type properties
2. Describe HAB-2 type properties
3. When does Isaac Newton lease end?
4. What type of property does Robert Oppenheimer has?

Enter a prompt (or choose 1-4 from examples, 'q' to quit): 4

Query: What type of property does Robert Oppenheimer has?
Query result:
Robert Oppenheimer has a designated Triple Residential Pod of lunar surface property on the Schiaparelli Plaza Property.
```

Notice we've included some example prompts to help you get started. You can use these prompts or create your own.

Go ahead and execute the script `src/querying-documents.py` to see the data extraction process.

Take a look at the [workshop](src/querying-documents.py) script to see how to extract data from multiple documents.

