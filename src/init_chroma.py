import chromadb
import openai
from box_sdk_gen import BoxClient, SearchForContentContentTypes
from chromadb.errors import InvalidCollectionException
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.box import BoxReader
from llama_index.vector_stores.chroma import ChromaVectorStore

from utils.box_client_ccg import AppConfig, get_ccg_user_client


def main():
    conf = AppConfig()
    client: BoxClient = get_ccg_user_client(conf, conf.ccg_user_id)

    # who am i
    me = client.users.get_user_me()

    # cleat screen
    print("\033[H\033[J")
    print(f"Hello, I'm logged in as {me.name} ({me.id})\n")

    # Using BoxReader
    box_reader = BoxReader(client)

    leases_ids = box_reader.search_resources(
        query="HAB-",
        ancestor_folder_ids=[conf.box_root_demo_folder],
        content_types=[SearchForContentContentTypes.NAME],
        file_extensions=["docx"],
        limit=100,
    )

    print(f"Leases found: {len(leases_ids)}, reading documents...\n")
    # print(f"Leases ids: {leases_ids}")

    documents = box_reader.load_data(file_ids=leases_ids)

    # Setup model
    openai.api_key = conf.open_ai_key
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

    # Initialize ChromaDB (Vector store)
    chroma_client = chromadb.PersistentClient(path="./.chroma.db")
    try:
        chroma_collection = chroma_client.get_collection("workshop_leases")
    except InvalidCollectionException:
        chroma_collection = chroma_client.create_collection("workshop_leases")

    # Set up ChromaVectorStore and load in data
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create a Chroma Index
    print("Indexing documents...\n")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True,
    )

    print()

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


if __name__ == "__main__":
    main()
