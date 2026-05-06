import streamlit as st

def render():
    st.markdown("""
    <div style='padding: 2rem 0 1rem 0;'>
        <div class='pm-title'>Poetry<span style='color:#9333ea;'>Mind</span></div>
        <div class='pm-subtitle'>Where Artificial Intelligence Meets the Ancient Art of Verse</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)

    # Hero section
    col1, col2 = st.columns([3, 2], gap="large")
    
    with col1:
        st.markdown("""
        <div class='pm-card'>
            <div class='pm-heading'>What is PoetryMind?</div>
            <p style='color:#b8a8d8; line-height:1.9; font-size:1.05rem;'>
                PoetryMind is a full-stack AI platform that brings machine learning 
                to the world of poetry. Built on a corpus of <strong style='color:#c4a8f5;'>20,487 poems</strong> 
                spanning <strong style='color:#c4a8f5;'>136 forms</strong> and <strong style='color:#c4a8f5;'>144 topics</strong>, 
                it can analyze, classify, and generate poetry using state-of-the-art NLP techniques.
            </p>
            <p style='color:#b8a8d8; line-height:1.9; font-size:1.05rem;'>
                Whether you're a student, researcher, or poetry enthusiast — PoetryMind 
                gives you tools to explore the vast landscape of English verse.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample poem
        st.markdown("""
        <div style='margin-top:1rem;'>
            <div class='pm-heading' style='font-size:1.2rem;'>Featured Excerpt</div>
            <div class='poem-box'>
Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date.
            </div>
            <div style='color:#6050a0; font-size:0.85rem; margin-top:0.5rem; font-style:italic;'>
                — William Shakespeare, Sonnet 18
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='pm-card' style='height:100%;'>
            <div class='pm-heading' style='font-size:1.2rem;'>✦ Features</div>
            <div style='display:flex; flex-direction:column; gap:0.8rem; margin-top:0.8rem;'>
        """, unsafe_allow_html=True)
        
        features = [
            ("🔍", "Poem Form Classifier", "Identify sonnets, ballads, haikus & 17 more forms using ML"),
            ("💬", "Emotion Analyzer", "Detect joy, sadness, love, fear & more in any poem"),
            ("✨", "AI Poem Generator", "Generate original poems in any style using Markov chains"),
            ("📚", "Smart Recommendations", "Find similar poems via TF-IDF cosine similarity"),
            ("📊", "Analytics Dashboard", "Explore the dataset with interactive charts"),
        ]
        
        for icon, title, desc in features:
            st.markdown(f"""
            <div style='background:#0d0c20; border:1px solid #2a2050; border-radius:8px; padding:0.9rem;'>
                <div style='font-size:1.2rem; margin-bottom:0.3rem;'>{icon} <span style='color:#e0d0ff; font-size:1rem; font-weight:600;'>{title}</span></div>
                <div style='color:#7860a8; font-size:0.85rem; line-height:1.5;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)

    # Stats row
    st.markdown("""
    <div class='metric-row'>
        <div class='metric-box'>
            <div class='metric-val'>20,487</div>
            <div class='metric-label'>Total Poems</div>
        </div>
        <div class='metric-box'>
            <div class='metric-val'>136</div>
            <div class='metric-label'>Poetic Forms</div>
        </div>
        <div class='metric-box'>
            <div class='metric-val'>144</div>
            <div class='metric-label'>Topics</div>
        </div>
        <div class='metric-box'>
            <div class='metric-val'>57%</div>
            <div class='metric-label'>Classifier Accuracy</div>
        </div>
        <div class='metric-box'>
            <div class='metric-val'>8</div>
            <div class='metric-label'>Emotions Detected</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)
    
    # Tech stack
    st.markdown("<div class='pm-heading' style='font-size:1.2rem;'>Tech Stack</div>", unsafe_allow_html=True)
    techs = ["Python 3", "Streamlit", "Scikit-learn", "TF-IDF Vectorizer", "LinearSVC", 
             "Cosine Similarity", "Markov Chains", "Pandas", "Plotly", "NumPy"]
    badges = " ".join([f"<span class='pm-badge'>{t}</span>" for t in techs])
    st.markdown(f"<div style='margin-top:0.5rem;'>{badges}</div>", unsafe_allow_html=True)
