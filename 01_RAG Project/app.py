import streamlit as st
import os
import tempfile
import json
import hashlib

st.set_page_config(
    page_title="DocMind — PDF Assistant",
    page_icon="🧠",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

.stApp {
    background: #0b1120;
    color: #cbd5e1;
}

section[data-testid="stSidebar"] { display: none; }

.block-container {
    padding-top: 0 !important;
    max-width: 780px !important;
}

/* ── Header ── */
.app-header {
    background: linear-gradient(135deg, #0f2044 0%, #0d1b36 60%, #0a1628 100%);
    border-bottom: 1px solid #1e3a5f;
    padding: 2rem 2.5rem 1.8rem 2.5rem;
    margin: -1rem -1rem 2rem -1rem;
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(6,182,212,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.app-header::after {
    content: '';
    position: absolute;
    bottom: -20px; left: 30%;
    width: 300px; height: 100px;
    background: radial-gradient(ellipse, rgba(59,130,246,0.06) 0%, transparent 70%);
}
.app-logo {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #06b6d4;
    margin-bottom: 0.6rem;
}
.app-title {
    font-size: 1.9rem;
    font-weight: 700;
    color: #f0f6ff;
    line-height: 1.2;
    margin-bottom: 0.4rem;
}
.app-title span { color: #06b6d4; }
.app-subtitle {
    font-size: 0.88rem;
    color: #64748b;
    font-weight: 400;
}

/* ── Setup card ── */
.setup-card {
    background: #0f1d35;
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
    margin-bottom: 0.8rem;
}
.setup-card-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.step-badge {
    background: #0e3a5c;
    color: #06b6d4;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    border: 1px solid #1e5a7f;
}
.setup-card-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #94a3b8;
}

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: #0b1829 !important;
    border: 1px solid #1e3a5f !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #06b6d4 !important;
    box-shadow: 0 0 0 2px rgba(6,182,212,0.15) !important;
}
.stTextInput > div > div > input::placeholder { color: #334155 !important; }

/* ── File uploader ── */
div[data-testid="stFileUploader"] {
    background: #0b1829 !important;
    border: 1px dashed #1e3a5f !important;
    border-radius: 10px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0284c7, #06b6d4) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 12px rgba(6,182,212,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(6,182,212,0.35) !important;
}

/* ── Ready pill ── */
.pdf-ready-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #052e16;
    border: 1px solid #14532d;
    color: #4ade80;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
}
.pdf-ready-pill::before {
    content: '●';
    font-size: 0.6rem;
    animation: blink 2s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

/* ── Cache hit badge ── */
.cache-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: #1a2e1a;
    border: 1px solid #2d5a2d;
    color: #86efac;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    margin-left: 0.5rem;
    vertical-align: middle;
    letter-spacing: 0.04em;
}

/* ── Chat bubbles ── */
.msg-user {
    display: flex;
    justify-content: flex-end;
    gap: 0.7rem;
    align-items: flex-start;
    margin-bottom: 0.8rem;
}
.msg-user .bubble {
    background: linear-gradient(135deg, #0369a1, #0284c7);
    color: #f0f9ff;
    border-radius: 16px 16px 4px 16px;
    padding: 0.75rem 1.1rem;
    max-width: 75%;
    font-size: 0.9rem;
    line-height: 1.6;
    box-shadow: 0 2px 8px rgba(3,105,161,0.3);
}
.msg-user .avatar {
    width: 32px; height: 32px;
    background: #0369a1;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem;
    flex-shrink: 0;
    margin-top: 2px;
    font-weight: 700;
    color: #bae6fd;
}
.msg-ai {
    display: flex;
    justify-content: flex-start;
    gap: 0.7rem;
    align-items: flex-start;
    margin-bottom: 0.8rem;
}
.msg-ai .bubble {
    background: #0f1d35;
    border: 1px solid #1e3a5f;
    color: #cbd5e1;
    border-radius: 16px 16px 16px 4px;
    padding: 0.85rem 1.15rem;
    max-width: 80%;
    font-size: 0.9rem;
    line-height: 1.7;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.msg-ai .avatar {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #0e3a5c, #0284c7);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    margin-top: 2px;
    border: 1px solid #1e5a7f;
}

/* ── Section divider ── */
.section-divider {
    border: none;
    border-top: 1px solid #1e3a5f;
    margin: 1.5rem 0;
}

/* ── Source box ── */
.source-item {
    background: #0b1829;
    border: 1px solid #1e3a5f;
    border-left: 3px solid #06b6d4;
    border-radius: 6px;
    padding: 0.7rem 0.9rem;
    margin-top: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #64748b;
    line-height: 1.6;
}
.source-item b { color: #38bdf8; display: block; margin-bottom: 0.3rem; }

/* ── Cache stats bar ── */
.cache-stats {
    background: #0a1628;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    display: flex;
    gap: 1.5rem;
    font-size: 0.78rem;
    color: #475569;
    margin-bottom: 1rem;
}
.cache-stats span { color: #06b6d4; font-weight: 600; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    border: 1px dashed #1e3a5f;
    border-radius: 14px;
}
.empty-state .icon { font-size: 2.8rem; margin-bottom: 0.8rem; }
.empty-state .msg  { font-size: 0.9rem; color: #475569; }

/* ── Alerts ── */
.stAlert { border-radius: 8px !important; }

/* ── Footer ── */
.footer {
    margin-top: 3.5rem;
    padding: 1.2rem 0 0.8rem 0;
    border-top: 1px solid #1e3a5f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.6rem;
}
.footer-left { display: flex; flex-direction: column; gap: 0.15rem; }
.footer-name {
    font-size: 0.9rem;
    font-weight: 700;
    color: #e2e8f0;
}
.footer-tagline { font-size: 0.72rem; color: #334155; }
.footer-badges  { display: flex; gap: 0.4rem; flex-wrap: wrap; }
.footer-badge {
    background: #0f1d35;
    border: 1px solid #1e3a5f;
    border-radius: 999px;
    padding: 0.2rem 0.65rem;
    font-size: 0.68rem;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
}
</style>
""", unsafe_allow_html=True)



# CACHE SYSTEM 


CACHE_FILE = "qa_cache.json"

def load_cache() -> dict:
    """Load cache from JSON file. Returns empty dict if file doesn't exist."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache: dict):
    """Save cache to JSON file."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def make_cache_key(pdf_name: str, question: str) -> str:
    """
    Create a unique key per PDF + question.
    Uses MD5 hash so long questions stay clean as keys.
    Format: pdfname__<hash>
    """
    clean_q   = question.lower().strip()
    clean_pdf = pdf_name.lower().strip()
    raw       = f"{clean_pdf}::{clean_q}"
    return hashlib.md5(raw.encode()).hexdigest()

def get_cached_answer(pdf_name: str, question: str):
    """Return cached answer string if exists, else None."""
    cache = load_cache()
    key   = make_cache_key(pdf_name, question)
    return cache.get(key, None)

def store_answer(pdf_name: str, question: str, answer: str):
    """Save a new Q&A pair to the cache."""
    cache       = load_cache()
    key         = make_cache_key(pdf_name, question)
    cache[key]  = answer
    save_cache(cache)

def get_cache_size() -> int:
    """Return how many Q&A pairs are currently cached."""
    return len(load_cache())



# SESSION STATE

if "rag_chain"    not in st.session_state: st.session_state.rag_chain    = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "pdf_name"     not in st.session_state: st.session_state.pdf_name     = None



# BUILD RAG CHAIN

def build_rag_chain(pdf_path, groq_api_key):
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import FastEmbedEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain

    pages  = PyPDFLoader(pdf_path).load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(pages)
    vs     = Chroma.from_documents(chunks, FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5"))
    ret    = vs.as_retriever(search_kwargs={"k": 5})
    llm    = ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=groq_api_key)

    prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant. Use the context below to answer the question clearly and concisely.
If context is partial, combine ideas and summarize logically.
If you don't know, say so honestly.

Context:
{context}

Question:
{input}
""")
    chain = create_retrieval_chain(ret, create_stuff_documents_chain(llm, prompt))
    return chain, len(pages), len(chunks)



# HEADER

st.markdown("""
<div class="app-header">
    <div class="app-logo">🧠 DocMind</div>
    <div class="app-title">Chat with your <span>PDF</span></div>
    <div class="app-subtitle">Upload a document and get instant AI-powered answers — Groq · LangChain · RAG</div>
</div>
""", unsafe_allow_html=True)



# STEP 1 — API KEY

groq_api_key = ""
try:
    groq_api_key = st.secrets.get("GROQ_API_KEY", "")
except:
    pass

if not groq_api_key:
    # No secret found — show Step 1 input as fallback
    st.markdown("""
    <div class="setup-card">
        <div class="setup-card-header">
            <span class="step-badge">STEP 01</span>
            <span class="setup-card-title">Connect your Groq API Key</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    groq_api_key = st.text_input("API Key", type="password", placeholder="gsk_...", label_visibility="collapsed")
    st.caption("🔑 [Get a free key at console.groq.com →](https://console.groq.com)")
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# If secret IS set → Step 1 is completely hidden, user sees Step 2 directly



# STEP 2 — UPLOAD PDF (becomes STEP 01 when secret is set)

upload_step = "STEP 01" if groq_api_key else "STEP 02"
st.markdown(f"""
<div class="setup-card">
    <div class="setup-card-header">
        <span class="step-badge">{upload_step}</span>
        <span class="setup-card-title">Upload your PDF document</span>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

if uploaded_file and groq_api_key:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"📎 **{uploaded_file.name}**")
    with col2:
        process_btn = st.button("⚡ Process", use_container_width=True)

    if process_btn:
        with st.spinner("Indexing your PDF..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                chain, n_pages, n_chunks = build_rag_chain(tmp_path, groq_api_key)
                st.session_state.rag_chain    = chain
                st.session_state.pdf_name     = uploaded_file.name
                st.session_state.chat_history = []
                os.unlink(tmp_path)
                st.success(f"✅ {n_pages} pages · {n_chunks} chunks — Ready to chat!")
            except Exception as e:
                st.error(f"❌ {str(e)}")

elif uploaded_file and not groq_api_key:
    st.warning("⚠️ Please enter your Groq API key above first.")

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)



# STEP 3 — CHAT

if st.session_state.rag_chain:

    st.markdown(f'<div class="pdf-ready-pill">{st.session_state.pdf_name}</div>', unsafe_allow_html=True)

    # Cache stats bar
    total_cached = get_cache_size()
    st.markdown(f"""
    <div class="cache-stats">
        ⚡ Smart Cache &nbsp;·&nbsp; <span>{total_cached}</span> answers saved &nbsp;·&nbsp; Same question = instant reply, zero tokens used
    </div>
    """, unsafe_allow_html=True)

    # Suggestion chips (only when no chat yet)
    chosen = None
    if not st.session_state.chat_history:
        st.markdown("**Try asking:**")
        chip_cols = st.columns(3)
        suggestions = ["Summarize this document", "What are the key topics?", "Explain the main concepts"]
        for i, sug in enumerate(suggestions):
            with chip_cols[i]:
                if st.button(sug, key=f"chip_{i}"):
                    chosen = sug

    # Chat history bubbles
    for item in st.session_state.chat_history:
        # User bubble
        st.markdown(f"""
        <div class="msg-user">
            <div class="bubble">{item['q']}</div>
            <div class="avatar">YP</div>
        </div>
        """, unsafe_allow_html=True)

        # AI bubble — show cache badge if it was a cache hit
        cache_tag = '<span class="cache-badge">⚡ cached</span>' if item.get("from_cache") else ""
        st.markdown(f"""
        <div class="msg-ai">
            <div class="avatar">🧠</div>
            <div class="bubble">{item['a']}{cache_tag}</div>
        </div>
        """, unsafe_allow_html=True)

        # Sources (only available for non-cached answers)
        if item.get("sources"):
            with st.expander("📎 View sources"):
                for i, doc in enumerate(item["sources"]):
                    page = doc.metadata.get("page", "?")
                    st.markdown(f'<div class="source-item"><b>Source {i+1} — Page {page}</b>{doc.page_content[:300]}...</div>', unsafe_allow_html=True)

    # Input bar
    st.markdown("")
    col1, col2 = st.columns([5, 1])
    with col1:
        question = st.text_input("Ask", placeholder="Ask anything about your document...", label_visibility="collapsed")
    with col2:
        ask_btn = st.button("Send →", use_container_width=True)

    final_question = chosen or (question if ask_btn and question else None)

    if final_question:
        # ── Check cache first ──────────────────────────────
        cached_answer = get_cached_answer(st.session_state.pdf_name, final_question)

        if cached_answer:
            # Cache HIT — no API call!
            st.session_state.chat_history.append({
                "q":          final_question,
                "a":          cached_answer,
                "sources":    [],
                "from_cache": True
            })
            st.rerun()

        else:
            # Cache MISS — call Groq API
            with st.spinner("Thinking... 🤔"):
                try:
                    response = st.session_state.rag_chain.invoke({"input": final_question})
                    answer   = response["answer"]
                    sources  = response.get("context", [])

                    # Save to persistent cache
                    store_answer(st.session_state.pdf_name, final_question, answer)

                    st.session_state.chat_history.append({
                        "q":          final_question,
                        "a":          answer,
                        "sources":    sources,
                        "from_cache": False
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {str(e)}")

    # Clear chat button
    if st.session_state.chat_history:
        st.markdown("")
        col_a, col_b = st.columns([4, 1])
        with col_b:
            if st.button("🗑️ Clear chat"):
                st.session_state.chat_history = []
                st.rerun()

else:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">💬</div>
        <div class="msg">Complete Steps 1 and 2 above to start chatting with your PDF.</div>
    </div>
    """, unsafe_allow_html=True)



# FOOTER

st.markdown("""
<div class="footer">
    <div class="footer-left">
        <div class="footer-name">Yubraj Parajuli</div>
        <div class="footer-tagline">Built with LangChain · Groq · Streamlit</div>
    </div>
    <div class="footer-badges">
        <span class="footer-badge">LangChain</span>
        <span class="footer-badge">Groq LLM</span>
        <span class="footer-badge">ChromaDB</span>
        <span class="footer-badge">FastEmbed</span>
        <span class="footer-badge">Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)
