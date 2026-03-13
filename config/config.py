import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # loads .env file if present

def get_secret(key):
    """Retrieve secret from environment variables or Streamlit secrets."""
    # 1. Check environment variables first (for local/server .env files)
    env_val = os.getenv(key)
    if env_val:
        return env_val
    
    # 2. Check Streamlit secrets (for Streamlit Cloud)
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        # Streamlit raises an error if secrets are accessed but not configured
        pass
        
    return None

GROQ_API_KEY   = get_secret("GROQ_API_KEY")
TAVILY_API_KEY = get_secret("TAVILY_API_KEY")