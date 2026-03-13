import streamlit as st
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from models.embeddings import get_embeddings

embeddings = get_embeddings()

def get_session_paths():
    """Create and return paths specific to the current user session."""
    session_id = st.session_state.get("session_id", "default")
    # Store session-specific data in temp folders
    base_data = os.path.join("temp_data", session_id)
    base_index = os.path.join("temp_index", session_id)
    os.makedirs(base_data, exist_ok=True)
    os.makedirs(base_index, exist_ok=True)
    return base_data, base_index

def load_and_index_documents():
    """Index documents specifically for this session."""
    data_dir, index_dir = get_session_paths()

    try:
        if not os.path.exists(data_dir) or not os.listdir(data_dir):
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

        vector_store = FAISS.from_documents(splits, embeddings)
        # Store index in session folder
        vector_store.save_local(index_dir)
        st.session_state.vector_store_ready = True
        return vector_store

    except Exception as e:
        print(f"RAG indexing failed: {str(e)}")
        return None

def retrieve_relevant_docs(query: str, k: int = 5):
    """Retrieve docs only from this session's index."""
    _, index_dir = get_session_paths()
    
    try:
        # Check if the session index exists
        if not os.path.exists(os.path.join(index_dir, "index.faiss")):
            return []

        vector_store = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
        return vector_store.similarity_search(query, k=k)
    except Exception as e:
        print(f"RAG retrieval failed: {str(e)}")
        return []