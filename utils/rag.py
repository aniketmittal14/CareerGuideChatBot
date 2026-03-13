from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from models.embeddings import get_embeddings
import os

embeddings = get_embeddings()
_vector_store = None

def load_and_index_documents(data_dir: str = "data"):
    global _vector_store

    try:
        if _vector_store is not None:
            return _vector_store

        if not os.path.exists(data_dir):
            return None

        loader = PyPDFDirectoryLoader(data_dir)
        docs = loader.load()

        if not docs:
            return None

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        splits = text_splitter.split_documents(docs)

        _vector_store = FAISS.from_documents(splits, embeddings)
        return _vector_store

    except Exception as e:
        print(f"RAG indexing failed: {str(e)}")
        return None


def retrieve_relevant_docs(query: str, k: int = 5):
    try:
        if _vector_store is None:
            load_and_index_documents()  # lazy load

        if _vector_store is None:
            return []

        return _vector_store.similarity_search(query, k=k)
    except Exception as e:
        print(f"RAG retrieval failed: {str(e)}")
        return []