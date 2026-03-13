# 💼 Career Guide AI – Indian Students & Freshers

An AI-powered career assistant designed to help Indian students and freshers navigate jobs, resumes, interviews, and government schemes. Built with **RAG (Retrieval-Augmented Generation)** and **Live Web Search** for the most up-to-date career advice.

## 🚀 Features
- **RAG (Retrieval-Augmented Generation):** Upload career-related PDFs (resume guides, scheme documents, interview banks) to get context-aware answers.
- **Live Web Search:** Integrated with **Tavily AI** to find current job openings, salary trends, and news for 2025-2026.
- **Dual Response Modes:** Choose between **Concise** (quick answers) and **Detailed** (in-depth guidance) modes.
- **Indian Context:** Specifically tuned to provide advice relevant to the Indian job market and government initiatives.

## 🛠️ Tech Stack
- **Framework:** Streamlit
- **LLM:** Groq (Llama 3.3 70B)
- **Embeddings:** HuggingFace (all-MiniLM-L6-v2)
- **Vector Store:** FAISS
- **Search:** Tavily AI
- **Orchestration:** LangChain

## 📋 Prerequisites
- Python 3.10+
- [Groq API Key](https://console.groq.com/)
- [Tavily API Key](https://tavily.com/)

## ⚙️ Local Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/aniketmittal14/CareerGuideChatBot.git
   cd CareerGuideChatBot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## 🌐 Deployment (Streamlit Cloud)
1. Push this code to your GitHub repository.
2. Connect the repository to [Streamlit Cloud](https://share.streamlit.io/).
3. In **Advanced Settings > Secrets**, add your API keys in TOML format:
   ```toml
   GROQ_API_KEY = "your_actual_key"
   TAVILY_API_KEY = "your_actual_key"
   ```

## 📄 License
This project is part of the NeoStats Career Challenge.
