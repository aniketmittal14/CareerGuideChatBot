import os
from langchain_huggingface import HuggingFaceEmbeddings

# Suppress harmless "unexpected key" warnings from transformers
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

def get_embeddings():
    # Good 2025/2026 choices – fast & good quality
    model_name = "sentence-transformers/all-MiniLM-L6-v2"

    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},           # "cuda" if you have GPU
        encode_kwargs={"normalize_embeddings": True},
    )