import os
import streamlit as st
from dotenv import load_dotenv

# Try to load local .env if it exists
load_dotenv()

def get_secret(key, default=None):
    """
    Retrieve secret from Streamlit secrets or environment variables.
    Streamlit Cloud prioritizes secrets.toml/Secrets dashboard.
    """
    # 1. Try Streamlit Secrets (Cloud / .streamlit/secrets.toml)
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    # 2. Try Environment Variables (Local .env / System)
    return os.getenv(key, default)

GROQ_API_KEY   = get_secret("GROQ_API_KEY")
TAVILY_API_KEY = get_secret("TAVILY_API_KEY")