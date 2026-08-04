"""
RAG Chatbot — E-commerce Support (Lazada Domain)
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

# Thêm project root vào sys.path để import các task từ src/
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Lazada E-commerce Support RAG Chatbot",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .source-card {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 0.8rem;
        border-radius: 4px;
        margin-bottom: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR — INFO & SETTINGS
# =============================================================================

with st.sidebar:
    st.title("🛒 Lazada Support RAG")
    st.caption("Trợ lý hỏi đáp chính sách Lazada Vietnam (Đổi trả, LazPayLater, Phí người bán, Vận chuyển)")

    st.divider()

    st.subheader("💡 Câu hỏi gợi ý")
    suggestions = [
        "Thời hạn yêu cầu trả hàng hoàn tiền trên Lazada là bao lâu?",
        "Làm thế nào để kích hoạt và thanh toán ví LazPayLater?",
        "Thời gian giao hàng dự kiến và tra cứu vận đơn Lazada?",
        "Biểu phí dịch vụ và phí hoa hồng dành cho Nhà bán hàng?",
        "Chính sách bảo mật thông tin cá nhân của Lazada?",
        "Liên hệ Trợ lý ảo CLEO và Tổng đài hỗ trợ 1900 6509?",
    ]
    for s in suggestions:
        if st.button(s, use_container_width=True, key=f"sug_{hash(s)}"):
            st.session_state["pending_query"] = s

    st.divider()
    st.subheader("⚙️ Thiết Lập Pipeline")

    # Filter theo customer_role (Bonus +20% UI)
    role_options = {
        "Tất cả (Both)": "both",
        "Người mua (Buyer)": "buyer",
        "Người bán (Seller)": "seller"
    }
    selected_role_label = st.selectbox(
        "🎯 Đối tượng người dùng (customer_role)",
        options=list(role_options.keys()),
        index=0
    )
    customer_role = role_options[selected_role_label]

    top_k = st.slider("Số lượng tài liệu truy xuất (top_k)", min_value=3, max_value=10, value=5)

    st.divider()
    if st.button("🗑️ Xóa lịch sử trò chuyện", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("**Kiến trúc RAG Pipeline:**")
    st.caption("Semantic + BM25 ➔ RRF Rerank ➔ PageIndex Fallback (<0.48) ➔ LLM Citation")

# =============================================================================
# SESSION STATE
# =============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# =============================================================================
# MAIN CHAT AREA
# =============================================================================

st.markdown('<div class="main-header">🛒 Lazada E-commerce Support RAG Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Hệ thống hỏi đáp thông minh chính sách Lazada Vietnam hỗ trợ Người mua & Nhà bán hàng</div>', unsafe_allow_html=True)

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg and msg["sources"]:
            with st.expander(f"📚 Nguồn tham khảo ({len(msg['sources'])} chunks)"):
                for i, src in enumerate(msg["sources"], 1):
                    meta = src.get("metadata", {})
                    source_name = meta.get("source", "Unknown")
                    doc_type = meta.get("type", "unknown")
                    role = meta.get("customer_role", "both")
                    score = src.get("score", 0.0)
                    st.markdown(f"**[{i}] {source_name}** | Loại: `{doc_type}` | Role: `{role}` | Score: `{score:.4f}`")
                    st.text(src.get("content", "")[:350] + "...")
                    st.divider()

# =============================================================================
# QUERY HANDLING
# =============================================================================

user_input = st.chat_input("Nhập câu hỏi của bạn về chính sách/hỗ trợ Lazada...")
query = user_input or st.session_state.pending_query

if query:
    st.session_state.pending_query = None

    # Hiển thị câu hỏi của user
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Sinh câu trả lời từ RAG Pipeline
    with st.chat_message("assistant"):
        with st.spinner("🔍 Đang tìm kiếm chính sách và tổng hợp câu trả lời..."):
            answer = ""
            sources = []
            try:
                # Tích hợp Task 10 (Generation có Citation)
                from src.task10_generation import generate_with_citation
                response = generate_with_citation(query, top_k=top_k, customer_role=customer_role)
                answer = response.get("answer", "Không tìm thấy thông tin phù hợp.")
                sources = response.get("sources", [])

            except (ImportError, NotImplementedError):
                answer = (
                    "⚠️ **Task 10 (hoặc Task 8 & 9) chưa hoàn thành trong `src/`**\n\n"
                    "Khi Task 8, Task 9 và Task 10 hoàn tất, giao diện UI này sẽ tự động chạy 100% "
                    "và sinh câu trả lời đầy đủ kèm trích dẫn nguồn."
                )
                # Chạy thử demo retrieval đơn giản từ Task 7 nếu Task 10 chưa có
                try:
                    from src.task6_lexical_search import lexical_search
                    sources = lexical_search(query, top_k=top_k)
                except Exception:
                    sources = []

            except Exception as e:
                answer = f"❌ **Lỗi khi thực thi RAG Pipeline:** {e}"
                sources = []

            st.markdown(answer)

            if sources:
                with st.expander(f"📚 Nguồn tham khảo trích dẫn ({len(sources)} chunks)"):
                    for i, src in enumerate(sources, 1):
                        meta = src.get("metadata", {})
                        source_name = meta.get("source", "Unknown")
                        doc_type = meta.get("type", "unknown")
                        role = meta.get("customer_role", "both")
                        score = src.get("score", 0.0)
                        st.markdown(f"**[{i}] {source_name}** | Loại: `{doc_type}` | Role: `{role}` | Score: `{score:.4f}`")
                        st.text(src.get("content", "")[:350] + "...")
                        st.divider()

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })
