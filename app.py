"""
RAG Chatbot — Light Theme Customer Support UI (Lazada Domain)
Streamlit app kết nối RAG Retrieval (Task 9) và Generation (Task 10).

Chạy:
    streamlit run app.py
"""

import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Lazada Customer Support RAG Chatbot",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Light Theme CSS
st.markdown("""
<style>
    /* Global Light Background */
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
    }

    /* Sidebar Light */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 2px solid #E2E8F0;
    }
    section[data-testid="stSidebar"] * {
        color: #334155 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #0F172A !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }

    /* Page Title */
    .main-title {
        font-size: 2rem;
        font-weight: 800;
        color: #0369A1;
        margin-bottom: 0.2rem;
    }
    .main-sub {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }

    /* Chat Bubbles - Light Theme */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 14px !important;
        padding: 1.2rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
        color: #1E293B !important;
    }

    /* Assistant bubble accent */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        background-color: #F0FDF4 !important;
        border: 1.5px solid #86EFAC !important;
    }

    /* Chat Input - Light Theme */
    div[data-testid="stBottomBlockContainer"] {
        background: #F8FAFC !important;
        border-top: 2px solid #0284C7 !important;
        padding-top: 0.8rem !important;
    }
    div[data-testid="stChatInput"] {
        border: 2px solid #0284C7 !important;
        border-radius: 12px !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 2px 12px rgba(2, 132, 199, 0.15) !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #059669 !important;
        box-shadow: 0 0 16px rgba(5, 150, 105, 0.25) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #0F172A !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        background-color: #FFFFFF !important;
    }

    /* Badges */
    .source-badge {
        background-color: #0284C7;
        color: white;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 6px;
    }
    .role-badge {
        background-color: #059669;
        color: white;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown("### 🛒 Trung Tâm Hỗ Trợ Lazada")
    st.caption("Trợ lý tra cứu chính sách & tư vấn tự động")

    if st.button("🗑️ Xóa toàn bộ đoạn chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.subheader("⚙️ Bộ Lọc & Tìm Kiếm")

    role_options = {
        "🌐 Tất cả đối tượng (Both)": None,
        "🛒 Người mua hàng (Buyer)": "buyer",
        "🏪 Nhà bán hàng (Seller)": "seller"
    }
    selected_role_label = st.selectbox("Đối tượng cần tư vấn", options=list(role_options.keys()), index=0)
    customer_role = role_options[selected_role_label]

    top_k = st.slider("Số lượng tài liệu trích xuất (top_k)", min_value=3, max_value=10, value=5)

    st.divider()
    st.caption("**Kiến trúc RAG Pipeline:**")
    st.caption("Semantic + BM25 ➔ RRF Rerank ➔ PageIndex Fallback ➔ LLM Citation")

# =============================================================================
# SESSION STATE
# =============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =============================================================================
# MAIN CHAT INTERFACE
# =============================================================================

st.markdown('<div class="main-title">🛒 CỔNG TƯ VẤN & HỖ TRỢ KHÁCH HÀNG LAZADA</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Hệ thống tra cứu chính thức Đổi trả, Ví LazPayLater, Vận chuyển & Biểu phí Nhà bán hàng</div>', unsafe_allow_html=True)

if not st.session_state.messages:
    st.info("👋 Chào bạn! Hãy nhập câu hỏi vào khung chat bên dưới để Trợ lý giải đáp ngay lập tức.")

for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🛒"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

        if msg["role"] == "assistant" and "sources" in msg and msg["sources"]:
            ret_src = msg.get("retrieval_source", "hybrid").upper()
            with st.expander(f"📚 Nguồn tham khảo ({len(msg['sources'])} tài liệu | Phương thức: {ret_src})"):
                for idx, src in enumerate(msg["sources"], 1):
                    meta = src.get("metadata", {}) or {}
                    doc_name = meta.get("source") or meta.get("document") or src.get("source") or f"Tài liệu {idx}"
                    doc_type = meta.get("type", "unknown")
                    role = meta.get("customer_role", "both")
                    score = src.get("score", 0.0)
                    st.markdown(
                        f"**[{idx}] {doc_name}** | "
                        f"<span class='source-badge'>{doc_type.upper()}</span> "
                        f"<span class='role-badge'>{role.upper()}</span> "
                        f"| Điểm: `{score:.4f}`",
                        unsafe_allow_html=True
                    )
                    st.text(src.get("content", "").strip()[:350] + "...")
                    st.divider()

# =============================================================================
# CHAT INPUT & EXECUTION
# =============================================================================

query = st.chat_input("💬 Nhập câu hỏi về chính sách Lazada tại đây...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(query)

    with st.chat_message("assistant", avatar="🛒"):
        with st.spinner("🔍 Đang tra cứu tài liệu và tổng hợp câu trả lời..."):
            answer = ""
            sources = []
            retrieval_source = "hybrid"

            try:
                from src.task10_generation import generate_with_citation
                res = generate_with_citation(query, top_k=top_k, customer_role=customer_role)
                answer = res.get("answer", "Tôi không thể xác minh thông tin này từ nguồn hiện có.")
                sources = res.get("sources", [])
                retrieval_source = res.get("retrieval_source", "hybrid")
            except Exception as e:
                answer = f"❌ **Lỗi xử lý RAG Pipeline:** {e}"
                sources = []
                retrieval_source = "error"

            st.markdown(answer)

            if sources:
                ret_src = retrieval_source.upper()
                with st.expander(f"📚 Nguồn tham khảo ({len(sources)} tài liệu | Phương thức: {ret_src})"):
                    for idx, src in enumerate(sources, 1):
                        meta = src.get("metadata", {}) or {}
                        doc_name = meta.get("source") or meta.get("document") or src.get("source") or f"Tài liệu {idx}"
                        doc_type = meta.get("type", "unknown")
                        role = meta.get("customer_role", "both")
                        score = src.get("score", 0.0)
                        st.markdown(
                            f"**[{idx}] {doc_name}** | "
                            f"<span class='source-badge'>{doc_type.upper()}</span> "
                            f"<span class='role-badge'>{role.upper()}</span> "
                            f"| Điểm: `{score:.4f}`",
                            unsafe_allow_html=True
                        )
                        st.text(src.get("content", "").strip()[:350] + "...")
                        st.divider()

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "retrieval_source": retrieval_source
    })
