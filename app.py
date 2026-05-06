import streamlit as st

st.set_page_config(
    page_title="PoetryMind",
    page_icon="🖋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:ital,wght@0,300;0,400;1,300&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Source Serif 4', Georgia, serif;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0d0d1a 0%, #1a1230 100%);
    border-right: 1px solid #2d2050;
}
[data-testid="stSidebar"] * { color: #e8e0f5 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size: 1rem;
    padding: 0.3rem 0;
    font-family: 'Source Serif 4', serif;
    letter-spacing: 0.03em;
}

/* Main background */
.stApp {
    background: #0a0a14;
    color: #e8e0f5;
}

/* Cards */
.pm-card {
    background: linear-gradient(135deg, #12112a 0%, #1c1535 100%);
    border: 1px solid #2d2050;
    border-radius: 12px;
    padding: 2rem;
    margin: 1rem 0;
}

/* Title styling */
.pm-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 3.5rem;
    font-weight: 700;
    color: #f5e6ff;
    line-height: 1.1;
    letter-spacing: -0.02em;
}
.pm-subtitle {
    font-family: 'Playfair Display', Georgia, serif;
    font-style: italic;
    color: #a78bca;
    font-size: 1.2rem;
    letter-spacing: 0.05em;
}
.pm-heading {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.8rem;
    color: #f0e0ff;
    margin-bottom: 0.5rem;
}

/* Poem display box */
.poem-box {
    background: #0d0c20;
    border-left: 3px solid #7c5cbf;
    border-radius: 0 8px 8px 0;
    padding: 1.5rem 2rem;
    font-style: italic;
    font-size: 1.05rem;
    color: #ddd4f5;
    white-space: pre-wrap;
    line-height: 1.9;
    letter-spacing: 0.01em;
}

/* Metric cards */
.metric-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}
.metric-box {
    background: linear-gradient(135deg, #1e1540 0%, #2a1f55 100%);
    border: 1px solid #3d2f70;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    flex: 1;
    min-width: 120px;
    text-align: center;
}
.metric-val {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #c4a8f5;
}
.metric-label {
    font-size: 0.8rem;
    color: #9080b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}

/* Badge */
.pm-badge {
    display: inline-block;
    background: #3d2f70;
    color: #c4a8f5;
    border-radius: 20px;
    padding: 0.2rem 0.9rem;
    font-size: 0.85rem;
    letter-spacing: 0.03em;
    margin: 0.2rem;
}

/* Confidence bar */
.conf-bar-wrap {
    margin: 0.3rem 0;
}
.conf-label {
    display: flex;
    justify-content: space-between;
    color: #c4a8f5;
    font-size: 0.9rem;
    margin-bottom: 0.2rem;
}
.conf-bar-bg {
    background: #1e1540;
    border-radius: 4px;
    height: 8px;
}
.conf-bar-fill {
    background: linear-gradient(90deg, #6b46c1, #c084fc);
    border-radius: 4px;
    height: 8px;
    transition: width 0.5s ease;
}

/* Recommendation card */
.rec-card {
    background: #12102a;
    border: 1px solid #2a2050;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 0.7rem 0;
}
.rec-type {
    color: #a78bca;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}
.rec-excerpt {
    color: #ccc4e8;
    font-style: italic;
    font-size: 0.95rem;
    line-height: 1.7;
}

/* Divider */
.pm-divider {
    border: none;
    border-top: 1px solid #2d2050;
    margin: 1.5rem 0;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6b46c1 0%, #9333ea 100%);
    color: white !important;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-family: 'Source Serif 4', serif;
    font-size: 1rem;
    letter-spacing: 0.03em;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #7c5cbf 0%, #a855f7 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(147, 51, 234, 0.4);
}

/* Inputs */
.stTextArea textarea, .stTextInput input {
    background: #12102a !important;
    border: 1px solid #2d2050 !important;
    border-radius: 8px !important;
    color: #e8e0f5 !important;
    font-family: 'Source Serif 4', serif !important;
}
.stSelectbox select, [data-baseweb="select"] {
    background: #12102a !important;
    color: #e8e0f5 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0d0c20;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: #1a1535;
    color: #9080b8;
    border-radius: 6px 6px 0 0;
}
.stTabs [aria-selected="true"] {
    background: #2d2050 !important;
    color: #e8e0f5 !important;
}

/* Slider */
.stSlider .st-cc { background: #6b46c1; }

/* Success/info */
.stSuccess, .stInfo {
    background: #1a1535 !important;
    border: 1px solid #2d2050 !important;
    color: #e8e0f5 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem 0;'>
        <div style='font-size:2.5rem;'>🖋️</div>
        <div style='font-family:"Playfair Display",serif; font-size:1.4rem; color:#f0e0ff; font-weight:700;'>PoetryMind</div>
        <div style='font-size:0.8rem; color:#7060a0; font-style:italic; letter-spacing:0.08em;'>AI Poetry Analysis Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color:#2d2050; margin-bottom:1rem;'>", unsafe_allow_html=True)
    
    page = st.radio(
        "Navigate",
        ["🏠  Home", "🔍  Classifier", "💬  Emotion Analyzer", "✨  Poem Generator", "📚  Recommendations", "📊  Analytics Dashboard"],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr style='border-color:#2d2050; margin-top:2rem;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.75rem; color:#4a3870; text-align:center; line-height:1.6;'>
        20,487 poems · 136 forms · 144 topics<br>
        Powered by ML + NLP
    </div>
    """, unsafe_allow_html=True)

# ─── Page Routing ─────────────────────────────────────────────────────────────
page_key = page.split("  ")[1] if "  " in page else page

if page_key == "Home":
    from pages import home
    home.render()
elif page_key == "Classifier":
    from pages import classifier
    classifier.render()
elif page_key == "Emotion Analyzer":
    from pages import emotion
    emotion.render()
elif page_key == "Poem Generator":
    from pages import generator
    generator.render()
elif page_key == "Recommendations":
    from pages import recommendations
    recommendations.render()
elif page_key == "Analytics Dashboard":
    from pages import analytics
    analytics.render()
