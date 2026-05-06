import streamlit as st
import sys
sys.path.append('..')
from utils.helpers import predict_form, detect_emotion

EXAMPLE_POEMS = {
    "Sonnet (Shakespeare)": """Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date.""",
    "Haiku (Bashō)": """An old silent pond
A frog jumps into the pond
Splash! Silence again""",
    "Ballad": """There lived a wife at Usher's Well,
And a wealthy wife was she;
She had three stout and stalwart sons,
And sent them o'er the sea.""",
    "Limerick": """There was an Old Man with a beard,
Who said, 'It is just as I feared!
Two Owls and a Hen,
Four Larks and a Wren,
Have all built their nests in my beard!'""",
    "Free Verse (Whitman)": """I celebrate myself, and sing myself,
And what I assume you shall assume,
For every atom belonging to me as good belongs to you.
I loafe and invite my soul,
I lean and loafe at my ease observing a spear of summer grass.""",
}

def render():
    st.markdown("""
    <div style='padding:1.5rem 0 1rem 0;'>
        <div class='pm-title' style='font-size:2.5rem;'>🔍 Poem Form <span style='color:#9333ea;'>Classifier</span></div>
        <div class='pm-subtitle'>Identify the poetic form of any poem using Machine Learning</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")
    
    with col1:
        st.markdown("<div class='pm-heading' style='font-size:1.2rem;'>Input Poem</div>", unsafe_allow_html=True)
        
        # Example selector
        example_choice = st.selectbox(
            "Load an example poem (optional)",
            ["— type your own —"] + list(EXAMPLE_POEMS.keys()),
        )
        
        default_text = EXAMPLE_POEMS.get(example_choice, "") if example_choice != "— type your own —" else ""
        
        poem_input = st.text_area(
            "Paste or type your poem here",
            value=default_text,
            height=280,
            placeholder="Enter any poem here...\n\nShall I compare thee to a summer's day?\nThou art more lovely and more temperate...",
            label_visibility="collapsed"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            classify_btn = st.button("🔍 Classify Form", use_container_width=True)
        with col_btn2:
            clear_btn = st.button("✕ Clear", use_container_width=True)

    with col2:
        st.markdown("""
        <div class='pm-card'>
            <div class='pm-heading' style='font-size:1.1rem;'>ℹ️ About the Model</div>
            <ul style='color:#b8a8d8; line-height:1.9; font-size:0.9rem; margin:0; padding-left:1.2rem;'>
                <li>Trained on <strong style='color:#c4a8f5;'>1,998 poems</strong></li>
                <li><strong style='color:#c4a8f5;'>LinearSVC</strong> classifier with TF-IDF features</li>
                <li>Recognizes <strong style='color:#c4a8f5;'>20 poetic forms</strong></li>
                <li>~57% test accuracy across imbalanced classes</li>
                <li>Bigram features (1–2 word combinations)</li>
                <li>10,000 max TF-IDF features</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='pm-card' style='margin-top:1rem;'>
            <div class='pm-heading' style='font-size:1.1rem;'>📋 Recognizable Forms</div>
            <div style='margin-top:0.5rem;'>
        """, unsafe_allow_html=True)
        
        forms = ['Villanelle', 'Sonnet', 'Ballad', 'Haiku', 'Limerick', 'Dirge', 
                 'Epitaph', 'Elegy', 'Ode', 'Ballade', 'Free Verse', 'Quatrain',
                 'Italian Sonnet', 'Verse', 'Tetractys', 'Cavatina', 'Syllabic Verse',
                 'Kyrielle', 'Rondeau', 'Ghazal']
        badges = " ".join([f"<span class='pm-badge' style='font-size:0.75rem;'>{f}</span>" for f in forms])
        st.markdown(f"{badges}</div></div>", unsafe_allow_html=True)

    # Results
    if classify_btn and poem_input.strip():
        with st.spinner("Analyzing poem..."):
            pred_form, top_preds = predict_form(poem_input)
        
        st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align:center; padding:1.5rem;'>
            <div style='color:#9080b8; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.1em;'>Predicted Form</div>
            <div style='font-family:"Playfair Display",serif; font-size:3rem; color:#c4a8f5; font-weight:700; margin:0.3rem 0;'>{pred_form.replace('-',' ').title()}</div>
            <div style='color:#7060a0; font-size:0.9rem;'>Confidence: {top_preds[0][1]*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Confidence bars
        st.markdown("<div class='pm-card'><div class='pm-heading' style='font-size:1.1rem;'>Top 5 Predictions</div>", unsafe_allow_html=True)
        
        for form, prob in top_preds:
            pct = prob * 100
            st.markdown(f"""
            <div class='conf-bar-wrap'>
                <div class='conf-label'>
                    <span>{form.replace('-',' ').title()}</span>
                    <span>{pct:.1f}%</span>
                </div>
                <div class='conf-bar-bg'>
                    <div class='conf-bar-fill' style='width:{min(pct, 100):.1f}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Poem preview
        st.markdown(f"""
        <div style='margin-top:1rem;'>
            <div class='pm-heading' style='font-size:1.1rem;'>Your Poem</div>
            <div class='poem-box'>{poem_input[:600]}{'...' if len(poem_input)>600 else ''}</div>
        </div>
        """, unsafe_allow_html=True)
    
    elif classify_btn:
        st.warning("Please enter a poem to classify.")
