import streamlit as st
import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from models.llm import get_chatgroq_model
from config.config import GROQ_API_KEY
from utils.rag import load_and_index_documents, retrieve_relevant_docs, get_session_paths
from utils.web_search import perform_web_search
from utils.prompts import get_system_prompt

# ── Session Initialization ──────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

def get_chat_response(chat_model, messages, system_prompt):
    try:
        formatted = [SystemMessage(content=system_prompt)]
        for msg in messages:
            if msg["role"] == "user":
                formatted.append(HumanMessage(content=msg["content"]))
            else:
                formatted.append(AIMessage(content=msg["content"]))
        response = chat_model.invoke(formatted)
        return response.content
    except Exception as e:
        return f"Error generating response: {str(e)}"


def instructions_page():
    st.title("Career Guidance Chatbot – NeoStats Challenge")
    st.markdown("""
    ### Features implemented
    - **RAG** – answers from uploaded PDFs (schemes, resume guides, interview questions…)
    - **Live web search** – current job openings, news, salary trends (via Tavily)
    - **Concise / Detailed** response modes
    - PDF upload & on-demand indexing (Session-specific)
    - Source attribution

    ### Quick setup
    1. `pip install -r requirements.txt`
    2. Create `.env` file with your keys
    3. `streamlit run app.py`
    """)


def chat_page():
    st.title("💼 Career Guide AI – For Indian Students & Freshers")

    if not GROQ_API_KEY:
        st.error("GROQ_API_KEY not set. Check .env or Streamlit Cloud secrets.")
        return

    chat_model = get_chatgroq_model()

    # Get user-specific data directory
    data_dir, _ = get_session_paths()

    # ── Sidebar ─────────────────────────────────────────────────────────
    with st.sidebar:
        st.subheader("Response Style")
        mode = st.radio("Choose mode", ["Concise", "Detailed"], index=1).lower()

        st.subheader("Knowledge Base (RAG)")
        st.info("Your uploaded files are private to this session.")
        uploaded = st.file_uploader("Upload career PDFs", type="pdf", accept_multiple_files=True)

        if uploaded:
            # Clear old files if any (optional, for clean start)
            for file in uploaded:
                path = os.path.join(data_dir, file.name)
                with open(path, "wb") as f:
                    f.write(file.getvalue())
            
            if st.button("Index / Re-index Documents"):
                with st.spinner("Indexing your documents..."):
                    vs = load_and_index_documents()
                    if vs is None:
                        st.warning("No documents found or indexing failed.")
                    else:
                        st.success("Documents indexed!")

        st.divider()
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    # ── Chat ────────────────────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about jobs, resume, interviews, schemes, skills..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # RAG retrieval (session-specific)
                    docs = retrieve_relevant_docs(prompt, k=5)
                    context = "\n\n".join(d.page_content for d in docs) if docs else ""
                    sources = ""
                    if docs:
                        sources = "**From your documents:**\n" + "\n".join(
                            f"• {os.path.basename(d.metadata.get('source','file'))}" for d in docs
                        ) + "\n\n"

                    # Web search enrichment
                    web_text = ""
                    trigger_keywords = ["latest", "current", "202", "opening", "news", "salary", "job", "vacancy"]
                    if not context.strip() or any(kw in prompt.lower() for kw in trigger_keywords):
                        web_text = perform_web_search(prompt)
                        if not web_text.startswith("("):
                            context += f"\n\n**Recent web info:**\n{web_text}"
                            sources += "**Web sources** (Tavily): included above\n\n"

                    full_context = context.strip()

                    # Prepare prompt
                    full_user_msg = f"Context (use if relevant):\n{full_context}\n\nQuestion: {prompt}"

                    system = get_system_prompt(mode)

                    response_text = get_chat_response(
                        chat_model,
                        [{"role": "user", "content": full_user_msg}],
                        system
                    )

                    final = response_text
                    if sources:
                        final += "\n\n---\n**Sources**\n" + sources

                    st.markdown(final)
                    st.session_state.messages.append({"role": "assistant", "content": final})

                except Exception as e:
                    st.error(f"Error: {str(e)}")


def main():
    st.set_page_config(
        page_title="Career Guide AI – NeoStats Challenge",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to", ["Chat", "Instructions"], index=0)

    if page == "Instructions":
        instructions_page()
    else:
        chat_page()


if __name__ == "__main__":
    main()