import chromadb
import openai
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from utils.box_client_ccg import AppConfig


def print_response(query, response):
    print()
    print()
    print("=" * 80)
    print(f"Query: {query}")
    print("-" * 80)
    print("Query result:")
    print(response)
    print("-" * 80)
    print()


def main():
    # App config and Box Client
    conf = AppConfig()

    # cleat screen
    print("\033[H\033[J")

    # Setup model
    openai.api_key = conf.open_ai_key
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

    # Initialize ChromaDB (Vector store)
    chroma_client = chromadb.PersistentClient(path="./.chroma.db")
    chroma_collection = chroma_client.get_collection("workshop_leases")

    # Set up ChromaVectorStore and load in data
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # Load a Chroma Index
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model)

    # Query Data
    query_engine = index.as_query_engine()
    query = "Describe the indexed documents"

    response = query_engine.query(query)
    print_response(query, response)

    # Example prompts
    example_prompts = [
        "What type of units are these?",
        "Which 5 contracts renew first?",
        "What is the monthly expected revenue for these units?",
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


if __name__ == "__main__":
    main()
