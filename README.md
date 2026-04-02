Secure Financial Document Intelligence Platform:
A high-performance Retrieval-Augmented Generation (RAG) system designed to extract grounded, citation-backed insights from complex financial documents.

🚀 Features
Contextual Intelligence: Leverages GPT-4 and LangChain to analyze SEC filings, earnings reports, and transcripts without fine-tuning.
Semantic Retrieval: Uses OpenAI embeddings and Chroma VectorDB to achieve 85% retrieval relevance (top-5 hit rate).
Secure Architecture: Implemented JWT-based authentication and role-based access to protect sensitive financial data.
High Performance: Backend powered by FastAPI with LRU caching, delivering low-latency responses (1-2s).

🛠️ Tech Stack
LLM Orchestration: LangChain, OpenAI API (GPT-4)
Vector Database: Chroma Backend: FastAPI, Pydantic, Python 
Security: JWT (JSON Web Tokens) 
Data Handling: PyPDF (for processing financial PDFs)

 📂 Project Structure
 auth.py: Handles JWT generation and user validation.
 pipeline.py: The core RAG logic for document embedding and retrieval.
 main.py: FastAPI entry point and API route definitions.
 vector_db/: Local storage for indexed document embeddings.
 
 📈 Impact
Reduced answer hallucinations by grounding responses in specific document citations.
Improved system efficiency by reducing redundant LLM calls through strategic caching.
