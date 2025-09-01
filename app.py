import os
import json
from datetime import date, timedelta


import httpx
import streamlit as st

# Hard Coded
API_BASE = os.getenv("API_BASE", "http://localhost:7000")


st.set_page_config(
    page_title="Overgo – Conversational Hotel Finder", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
/* Main container styling */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Header styling */
.header-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
}

.header-title {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.header-subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
    font-weight: 300;
}

/* Sidebar styling */
.css-1d391kg {
    background-color: #f8fafc;
    border-right: 2px solid #e2e8f0;
}

/* Chat input styling */
.stChatInput > div > div > textarea {
    border-radius: 25px;
    border: 2px solid #e2e8f0;
    padding: 15px 20px;
    font-size: 16px;
}

.stChatInput > div > div > textarea:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Button styling */
.stButton > button {
    border-radius: 12px;
    border: none;
    padding: 12px 24px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

/* Hotel card styling */
.hotel-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border: 1px solid #e2e8f0;
    transition: all 0.3s ease;
}

.hotel-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

/* Section headers */
.section-header {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 3px solid #667eea;
}

/* Metrics styling */
.metric-container {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 1rem;
}

/* Chat message styling */
.stChatMessage {
    border-radius: 12px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Success/Error message styling */
.stSuccess {
    border-radius: 12px;
    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
    color: white;
}

.stError {
    border-radius: 12px;
    background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
    color: white;
}

/* Link button styling */
.stLinkButton > a {
    border-radius: 12px;
    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
    color: white !important;
    text-decoration: none;
    padding: 12px 24px;
    font-weight: 600;
    transition: all 0.3s ease;
    display: inline-block;
    width: 100%;
    text-align: center;
    box-shadow: 0 2px 8px rgba(72, 187, 120, 0.3);
}

.stLinkButton > a:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(72, 187, 120, 0.4);
}

/* Input field styling */
.stTextInput > div > div > input,
.stDateInput > div > div > input,
.stNumberInput > div > div > input {
    border-radius: 12px;
    border: 2px solid #e2e8f0;
    padding: 12px 16px;
}

.stTextInput > div > div > input:focus,
.stDateInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Selectbox styling */
.stSelectbox > div > div {
    border-radius: 12px;
    border: 2px solid #e2e8f0;
}

.stSelectbox > div > div > div {
    border: none;
    padding: 8px 16px;
}

/* Sidebar styling improvements */
.css-1lcbmhc .css-1outpf7 {
    background-color: #f8fafc;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
}

/* Image styling */
img {
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

/* Footer styling */
.footer-caption {
    text-align: center;
    color: #64748b;
    font-style: italic;
    padding: 2rem 0;
    background-color: #f8fafc;
    border-radius: 12px;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Header with enhanced styling
st.markdown("""
<div class="header-container">
    <h1 class="header-title">✈️ Overgo</h1>
    <p class="header-subtitle">High‑touch hotel discovery powered by AI</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="section-header">🏨 Trip Details</div>', unsafe_allow_html=True)
    city = st.text_input("🌍 Destination", value="Lagos")
    today = date.today()
    check_in = st.date_input("📅 Check‑in", value=today + timedelta(days=7))
    check_out = st.date_input("📅 Check‑out", value=today + timedelta(days=9))
    adults = st.number_input("👥 Adults", min_value=1, value=2)
    max_budget = st.number_input("💰 Max budget (USD)", min_value=0, value=0)
    provider = st.selectbox("🔧 Provider (demo)", ["affiliate", "mock"], index=0)
    st.info("💡 Provider 'affiliate' deep‑links to a Booking.com search. Switch to 'mock' to remove links.")


if "chat" not in st.session_state:
    st.session_state.chat = []

# Chat input
user_msg = st.chat_input("Ask for a vibe, e.g., ‘romantic boutique with rooftop pool in Lagos under $300’…")
if user_msg:
    st.session_state.chat.append({"role": "user", "content": user_msg})

    # Panels
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="section-header">💬 Conversation</div>', unsafe_allow_html=True)
    for turn in st.session_state.chat:
        with st.chat_message(turn["role"]):
            st.write(turn["content"])

    if st.button("🔄 Generate search from chat →"):
        try:
            payload = {"history": st.session_state.chat}
            r = httpx.post(f"{API_BASE}/chat-to-query", json=payload, timeout=20)
            r.raise_for_status()
            q = r.json()
            # Override with sidebar when set
            if city:
                q["city"] = city
            q["check_in"] = str(check_in)
            q["check_out"] = str(check_out)
            q.setdefault("guests", {})["adults"] = int(adults)
            if max_budget:
                q["budget_max"] = int(max_budget)

            st.session_state.last_query = q
            st.success("✅ Search parameters prepared successfully!")

        except Exception as e:
            st.error(f"❌ Failed to parse chat → query: {e}")


with col2:
    st.markdown('<div class="section-header">🏨 Hotel Results</div>', unsafe_allow_html=True)
    q = st.session_state.get("last_query")

    # Button row with search and clear buttons
    button_col1, button_col2 = st.columns([2, 1])
    with button_col1:
        if st.button("🔍 Search hotels", type="primary"):
            q = q or {
                "city": city,
                "check_in": str(check_in),
                "check_out": str(check_out),
                "guests": {"adults": int(adults)},
                "budget_max": int(max_budget) if max_budget else None,
            }
            os.environ["PROVIDER"] = provider
            try:
                with st.spinner('🔍 Searching for the perfect hotels...'):
                    r = httpx.post(f"{API_BASE}/search", json=q, timeout=30)
                    r.raise_for_status()
                    data = r.json()
                    st.session_state.results = data.get("results", [])
                    if st.session_state.results:
                        st.success(f"✅ Found {len(st.session_state.results)} hotels!")
            except Exception as e:
                st.error(f"❌ Search failed: {e}")
    
    with button_col2:
        if st.button("🗑️ Clear results"):
            st.session_state.results = []
            if "last_query" in st.session_state:
                del st.session_state.last_query
            st.success("✅ Results cleared!")

    results = st.session_state.get("results", [])
    if results:
        st.markdown(f'<div style="color: #64748b; margin: 1rem 0;">Showing {len(results)} results</div>', unsafe_allow_html=True)
    
    for h in results:
        with st.container(border=True):
            cols = st.columns([1, 3, 1])
            with cols[0]:
                if h.get("image_url"):
                    st.image(h["image_url"], use_column_width=True)
                else:
                    st.markdown('<div style="background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e0 100%); height: 120px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 2rem;">🏨</div>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f'<h3 style="color: #2d3748; margin-bottom: 0.5rem;">{h["name"]}</h3>', unsafe_allow_html=True)
                st.markdown(f'<p style="color: #64748b; margin-bottom: 1rem;">📍 {h["city"]}</p>', unsafe_allow_html=True)
                if h.get("rating"):
                    rating_stars = "⭐" * int(float(h["rating"]))
                    st.markdown(f'<p style="margin-bottom: 0.5rem;">{rating_stars} <strong>{h["rating"]}</strong> ({h.get("review_count", "–")} reviews)</p>', unsafe_allow_html=True)
                if h.get("summary"):
                    st.markdown(f'<p style="color: #4a5568; line-height: 1.5;">{h["summary"]}</p>', unsafe_allow_html=True)
            with cols[2]:
                if h.get("price_total"):
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.metric("💰 Estimated Total", f"{h['currency']} {h['price_total']:.0f}")
                    st.markdown('</div>', unsafe_allow_html=True)
                b = h.get("booking") or {}
                if b.get("url"):
                    st.link_button(f"🔗 {b.get('label', 'Book Now')}", b["url"], use_container_width=True)

st.divider()
st.markdown("""
<div class="footer-caption">
    🌟 <strong>Demo Platform</strong><br>
    Chat → Structured Search → Curated Results → White‑label Booking Link<br>
    <em>Switch providers when your API keys are ready to go live!</em>
</div>
""", unsafe_allow_html=True)

























