from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY
import os

def get_chatgroq_model(
    model_name: str = "llama-3.3-70b-versatile",
    temperature: float = 0.65,
    max_tokens: int = 2048
) -> ChatGroq:
    api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found.\n"
            "Set it in:\n"
            "  • .env file\n"
            "  • config/config.py\n"
            "  • Streamlit Cloud secrets"
        )

    try:
        return ChatGroq(
            groq_api_key=api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq model: {str(e)}")