# RAG application - Indexing Box documents using LlamaIndex and ChromaDB

This is a simple example of how to index documents in a Box folder using LlamaIndex and ChromaDB.

## Workshop overview

This workshop provides a hands-on simple example to indexing and querying documents stored in Box using the LlamaIndex and ChromaDB tools. 

Participants will learn how to use the Box API to search for and retrieve documents from a designated folder, and then use LlamaIndex to process and structure the content for further analysis. 

The workshop highlights the ease of setting up a pipeline that reads files from Box, transforms them into document embeddings using a pre-trained Hugging Face model, and stores these embeddings in a ChromaDB vector store. 

This setup enables efficient querying of document contents, making it ideal for organizing and extracting insights from large collections of files.

## Use case and context

Imagine yourself creating an application to help a user manage leases for 50 properties. You have a set of lease documents in your Box account, and your application will help users to answer questions about a single or multiple documents, as wel as extract data from those documents.

The properties vary from a single communal bed room to a three bedroom apartment. The lease documents are in Word format and contain information about the property, the tenant, the landlord, and the lease terms.

## Workshop content

- [Getting started](getting-started.md): Set up your environment and generate sample data.
- [Indexing documents](indexing-documents.md): Index documents in a Box folder using LlamaIndex and ChromaDB.
- [Querying documents](querying-documents.md): Query documents in a Box folder using LlamaIndex and ChromaDB.

## Conclusion

This workshop demonstrated how to index and query documents stored in Box using LlamaIndex and ChromaDB. Participants gained hands-on experience in setting up a complete pipeline—from retrieving documents via the Box API to generating embeddings using a pre-trained model and storing these embeddings in a vector database for fast, flexible querying. 

The integration of these tools illustrates the power of combining cloud storage, AI-driven document processing, and vector databases to streamline content organization and extraction.
