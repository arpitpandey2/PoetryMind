import streamlit as st
import sys
sys.path.append('..')
from utils.helpers import generate_poem

STYLE_INFO = {
    'sonnet': {'lines': 14, 'desc': 'A 14-line poem with iambic pentameter, exploring themes of love and beauty.'},
    'haiku': {'lines': 3, 'desc': 'A three-line Japanese form capturing a moment in nature.'},
    'ballad': {'lines': 12, 'desc': 'A narrative poem telling a story, often with a refrain.'},
    'limerick': {'lines': 5, 'desc': 'A humorous five-line poem with AABBA rhyme scheme.'},
    'villanelle': {'lines': 10, 'desc': 'A 19-line poem with two refrains and specific rhyme scheme.'},
    'free-verse': {'lines': 10, 'desc': 'Unmetered, unrhymed verse with the freedom of prose.'},
    'elegy': {'lines': 12, 'desc': 'A mournful poem lamenting loss or death.'},
    'ode': {'lines': 12, 'desc': 'A lyrical poem in praise of a person, place, or thing.'},
    'general': {'lines': 10, 'desc': 'A free-flowing poem from the full poetic corpus.'},
}

THEMES = ['love', 'death', 'nature', 'time', 'beauty', 'war', 'hope', 'longing', 
          'solitude', 'memory', 'light', 'darkness', 'sea', 'autumn', 'heaven',
          'dreams', 'truth', 'freedom', 'grief', 'joy']

def render():
    st.markdown("""
    <div style='padding:1.5rem 0 1rem 0;'>
        <div class='pm-title' style='font-size:2.5rem;'>✨ Poem <span style='color:#9333ea;'>Generator</span></div>
        <div class='pm-subtitle'>Create original verse using Markov chain text generation</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 3], gap="large")
    
    with col1:
        st.markdown("""
        <div class='pm-card'>
            <div class='pm-heading' style='font-size:1.2rem;'>⚙️ Settings</div>
        """, unsafe_allow_html=True)
        
        style = st.selectbox(
            "Poetic Style",
            options=list(STYLE_INFO.keys()),
            format_func=lambda x: x.replace('-', ' ').title()
        )
        
        theme = st.selectbox(
            "Theme / Seed Word",
            options=["(none)"] + THEMES
        )
        theme_val = "" if theme == "(none)" else theme
        
        info = STYLE_INFO[style]
        num_lines = st.slider("Number of lines", 4, 20, info['lines'])
        
        st.markdown(f"""
        <div style='background:#0d0c20; border:1px solid #2a2050; border-radius:8px; 
                    padding:0.8rem; margin-top:0.5rem;'>
            <div style='color:#9080b8; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.08em;'>About this form</div>
            <div style='color:#c4a8f5; font-size:0.9rem; margin-top:0.3rem; line-height:1.6;'>{info['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        generate_btn = st.button("✨ Generate Poem", use_container_width=True)
        
        if generate_btn:
            with st.spinner("Summoning verse from the corpus..."):
                poem = generate_poem(style=style, theme=theme_val, num_lines=num_lines)
            st.session_state['generated_poem'] = poem
            st.session_state['poem_style'] = style
            st.session_state['poem_theme'] = theme_val
    
    with col2:
        st.markdown("""
        <div class='pm-heading' style='font-size:1.2rem;'>Generated Poem</div>
        """, unsafe_allow_html=True)
        
        if 'generated_poem' in st.session_state:
            poem = st.session_state['generated_poem']
            style_name = st.session_state.get('poem_style', style).replace('-',' ').title()
            theme_name = st.session_state.get('poem_theme', '') or 'General'
            
            st.markdown(f"""
            <div style='display:flex; gap:0.5rem; margin-bottom:0.8rem; flex-wrap:wrap;'>
                <span class='pm-badge'>📖 {style_name}</span>
                <span class='pm-badge'>🏷️ Theme: {theme_name.title()}</span>
                <span class='pm-badge'>📝 {len(poem.splitlines())} lines</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='poem-box' style='font-size:1.1rem; line-height:2;'>
{poem}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top:1rem;'>", unsafe_allow_html=True)
            st.download_button(
                "⬇️ Download Poem",
                data=f"Style: {style_name}\nTheme: {theme_name}\n\n{poem}",
                file_name=f"poetrymind_{style}.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:#0d0c20; border:1px dashed #2a2050; border-radius:12px; 
                        padding:4rem 2rem; text-align:center;'>
                <div style='font-size:3rem; margin-bottom:1rem;'>✨</div>
                <div style='color:#6050a0; font-size:1.1rem; font-style:italic;'>
                    Choose a style and click Generate<br>to summon original verse...
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)
    
    # How it works
    st.markdown("""
    <div class='pm-card'>
        <div class='pm-heading' style='font-size:1.2rem;'>🔬 How Markov Chain Generation Works</div>
        <div style='display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:1rem; margin-top:1rem;'>
            <div style='text-align:center; padding:1rem; background:#0d0c20; border-radius:8px;'>
                <div style='font-size:1.5rem;'>📚</div>
                <div style='color:#c4a8f5; font-size:0.85rem; margin-top:0.4rem;'><strong>1. Corpus</strong></div>
                <div style='color:#7060a0; font-size:0.8rem; margin-top:0.3rem;'>Train on poems from each style</div>
            </div>
            <div style='text-align:center; padding:1rem; background:#0d0c20; border-radius:8px;'>
                <div style='font-size:1.5rem;'>🔗</div>
                <div style='color:#c4a8f5; font-size:0.85rem; margin-top:0.4rem;'><strong>2. Bigrams</strong></div>
                <div style='color:#7060a0; font-size:0.8rem; margin-top:0.3rem;'>Build word-pair transition chains</div>
            </div>
            <div style='text-align:center; padding:1rem; background:#0d0c20; border-radius:8px;'>
                <div style='font-size:1.5rem;'>🎲</div>
                <div style='color:#c4a8f5; font-size:0.85rem; margin-top:0.4rem;'><strong>3. Sample</strong></div>
                <div style='color:#7060a0; font-size:0.8rem; margin-top:0.3rem;'>Randomly walk the chain</div>
            </div>
            <div style='text-align:center; padding:1rem; background:#0d0c20; border-radius:8px;'>
                <div style='font-size:1.5rem;'>📜</div>
                <div style='color:#c4a8f5; font-size:0.85rem; margin-top:0.4rem;'><strong>4. Format</strong></div>
                <div style='color:#7060a0; font-size:0.8rem; margin-top:0.3rem;'>Shape into poetic lines</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
