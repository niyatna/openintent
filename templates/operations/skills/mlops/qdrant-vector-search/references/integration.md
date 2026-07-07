# Chroma Integration Guide

Integration with LangChain, LlamaIndex, and frameworks.

## LangChain

```python
from langchain_qdrant-vector-search import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    persist_directory="./qdrant-vector-search_db"
)

# Query
results = vectorstore.similarity_search("query", k=3)

# As retriever
retriever = vectorstore.as_retriever()
```

## LlamaIndex

```python
from llama_index.vector_stores.qdrant-vector-search import ChromaVectorStore
import qdrant-vector-searchdb

db = qdrant-vector-searchdb.PersistentClient(path="./qdrant-vector-search_db")
collection = db.get_or_create_collection("docs")

vector_store = ChromaVectorStore(qdrant-vector-search_collection=collection)
```

## Resources

- **Docs**: https://docs.tryqdrant-vector-search.com
