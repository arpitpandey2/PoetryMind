import streamlit as st
import sys
sys.path.append('..')
from utils.helpers import get_recommendations

EXAMPLE_INPUTS = {
    "Romantic verse": "My love is like a red red rose that's newly sprung in June. My love is like a melody that's sweetly played in tune.",
    "Nature poem": "I wandered lonely as a cloud that floats on high o'er vales and hills, when all at once I saw a crowd, a host of golden daffodils.",
    "Dark verse": "Deep into that darkness peering, long I stood there wondering, fearing, doubting, dreaming dreams no mortals dare to dream before.",
    "Martial verse": "Half a league, half a league, half a league onward, all in the valley of Death rode the six hundred.",
}

def render():
    st.markdown("""
    <div style='padding:1.5rem 0 1rem 0;'>
        <div class='pm-title' style='font-size:2.5rem;'>📚 Poem <span style='color:#9333ea;'>Recommendations</span></div>
        <div class='pm-subtitle'>Discover similar poems using TF-IDF cosine similarity</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)

    col1, col2 = st.columns([5, 2], gap="large")
    
    with col1:
        example_choice = st.selectbox(
            "Load an example", ["— type your own —"] + list(EXAMPLE_INPUTS.keys())
        )
        default = EXAMPLE_INPUTS.get(example_choice, "") if example_choice != "— type your own —" else ""
        
        poem_input = st.text_area(
            "Enter a poem or excerpt",
            value=default,
            height=180,
            placeholder="Paste any poem or passage here, and we'll find similar poems from our corpus...",
            label_visibility="collapsed"
        )
        
        n_recs = st.slider("Number of recommendations", 3, 10, 5)
        
        rec_btn = st.button("📚 Find Similar Poems", use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class='pm-card'>
            <div class='pm-heading' style='font-size:1.1rem;'>🔬 How it Works</div>
            <div style='color:#b8a8d8; font-size:0.9rem; line-height:1.8;'>
                <div style='margin-bottom:0.6rem;'>
                    <strong style='color:#c4a8f5;'>1. Vectorize</strong><br>
                    <span style='color:#7060a0;'>Convert poems to TF-IDF vectors (5,000 features)</span>
                </div>
                <div style='margin-bottom:0.6rem;'>
                    <strong style='color:#c4a8f5;'>2. Compare</strong><br>
                    <span style='color:#7060a0;'>Compute cosine similarity to all 2,000 corpus poems</span>
                </div>
                <div>
                    <strong style='color:#c4a8f5;'>3. Rank</strong><br>
                    <span style='color:#7060a0;'>Return top-N most similar poems</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Results
    if rec_btn and poem_input.strip():
        with st.spinner("Searching 2,000 poems for similarity..."):
            results = get_recommendations(poem_input, top_n=n_recs)
        
        st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)
        
        if not results:
            st.warning("No sufficiently similar poems found. Try a longer input.")
        else:
            st.markdown(f"""
            <div style='color:#9080b8; font-size:0.9rem; margin-bottom:1rem;'>
                Found <strong style='color:#c4a8f5;'>{len(results)}</strong> similar poems
            </div>
            """, unsafe_allow_html=True)
            
            for i, result in enumerate(results, 1):
                excerpt = result['poem_text'][:350].strip()
                if len(result['poem_text']) > 350:
                    excerpt += '...'
                score_pct = result['score'] * 100
                poem_type = result['poem_type'].replace('-', ' ').title()
                
                # Similarity color
                if score_pct > 20:
                    sim_color = '#34d399'
                elif score_pct > 10:
                    sim_color = '#fbbf24'
                else:
                    sim_color = '#a78bfa'
                
                st.markdown(f"""
                <div class='rec-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;'>
                        <div style='display:flex; align-items:center; gap:0.7rem;'>
                            <span style='font-family:"Playfair Display",serif; font-size:1.3rem; color:#4a3870; font-weight:700;'>
                                {i:02d}
                            </span>
                            <span class='pm-badge'>{poem_type}</span>
                        </div>
                        <div style='display:flex; align-items:center; gap:0.4rem;'>
                            <span style='color:#6050a0; font-size:0.8rem;'>Similarity</span>
                            <span style='color:{sim_color}; font-weight:700; font-size:1rem;'>{score_pct:.1f}%</span>
                        </div>
                    </div>
                    <div class='conf-bar-bg' style='margin-bottom:0.8rem;'>
                        <div class='conf-bar-fill' style='width:{min(score_pct*3, 100):.0f}%; background:linear-gradient(90deg, {sim_color}55, {sim_color});'></div>
                    </div>
                    <div class='rec-excerpt'>{excerpt}</div>
                </div>
                """, unsafe_allow_html=True)
    
    elif rec_btn:
        st.warning("Please enter a poem to find recommendations.")
