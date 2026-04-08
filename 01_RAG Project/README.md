# 🔎 Retrieval-Augmented Generation (RAG) Chatbot

## 📌 Overview

This project is a Retrieval-Augmented Generation (RAG) system that allows users to interact with PDF documents and get accurate, context-aware answers. It combines document retrieval techniques with Large Language Models (LLMs) to improve response accuracy and reduce hallucinations.

---

## ⚙️ Tech Stack

- Python 🐍
- LangChain
- ChromaDB (Vector Database)
- FastEmbed (BAAI/bge-small-en-v1.5)
- Groq API (Llama-3.1-8B-Instant)
- Jupyter Notebook

---

## 🚀 Features

- 📄 Load and process PDF documents
- ✂️ Split text into optimized chunks
- 🧠 Generate embeddings for semantic understanding
- 🔍 Perform similarity search using vector database
- 🤖 Generate context-aware answers using LLM
- 💬 Interactive question-answering system

---

## 🧠 How It Works

1. PDF document is loaded into the system
2. Text is split into smaller overlapping chunks
3. Each chunk is converted into vector embeddings
4. Embeddings are stored in ChromaDB
5. User asks a question
6. Relevant chunks are retrieved based on similarity search
7. LLM generates a final answer using retrieved context

---

## 📚 Key Learnings

- Understanding of Retrieval-Augmented Generation (RAG)
- Vector databases and similarity search
- Role of embeddings in NLP
- Chunking strategies for better retrieval
- Integration of LLMs with external knowledge sources

---

## 📁 Project Structure

01_RAG_Project/
│
├── notebook.ipynb
├── README.md

## 🎯 Future Improvements

- Add Streamlit web interface
- Support multiple file formats (TXT, DOCX)
- Improve retrieval accuracy with advanced chunking
- Deploy as a web application

---

## 🙏 Acknowledgement

This project was built as part of my AI and Data Science learning journey under the guidance of **Angat Sitaula** and supported by online learning resources.

---

## 👨‍💻 Author

Yubraj Parajuli
