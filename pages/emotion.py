import streamlit as st
import plotly.graph_objects as go
import sys
sys.path.append('..')
from utils.helpers import detect_emotion

EMOTION_COLORS = {
    'Joy': '#fbbf24',
    'Sadness': '#60a5fa',
    'Love': '#f472b6',
    'Fear': '#a78bfa',
    'Anger': '#f87171',
    'Wonder': '#34d399',
    'Melancholy': '#94a3b8',
}

EMOTION_EMOJI = {
    'Joy': '☀️',
    'Sadness': '🌧️',
    'Love': '❤️',
    'Fear': '🌑',
    'Anger': '🔥',
    'Wonder': '✨',
    'Melancholy': '🍂',
}

EXAMPLE_POEMS = {
    "Joyful — Keats": """O Autumn! Season of mists and mellow fruitfulness!
Close bosom-friend of the maturing sun;
Conspiring with him how to load and bless
With fruit the vines that round the thatch-eaves run.""",
    "Sad — Shelley": """Music, when soft voices die,
Vibrates in the memory;
Odours, when sweet violets sicken,
Live within the sense they quicken.""",
    "Love — Byron": """She walks in beauty, like the night
Of cloudless climes and starry skies;
And all that's best of dark and bright
Meet in her aspect and her eyes.""",
    "Fear — Poe-like": """Deep into that darkness peering,
Long I stood there wondering, fearing,
Doubting, dreaming dreams no mortals
Dare to dream before.""",
}

def render():
    st.markdown("""
    <div style='padding:1.5rem 0 1rem 0;'>
        <div class='pm-title' style='font-size:2.5rem;'>💬 Emotion <span style='color:#9333ea;'>Analyzer</span></div>
        <div class='pm-subtitle'>Uncover the emotional landscape woven into verse</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")
    
    with col1:
        example_choice = st.selectbox(
            "Load example", ["— type your own —"] + list(EXAMPLE_POEMS.keys())
        )
        default = EXAMPLE_POEMS.get(example_choice, "") if example_choice != "— type your own —" else ""
        
        poem_input = st.text_area(
            "Paste your poem",
            value=default,
            height=250,
            placeholder="Enter any poem to analyze its emotional tone...",
            label_visibility="collapsed"
        )
        
        analyze_btn = st.button("💬 Analyze Emotions", use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class='pm-card'>
            <div class='pm-heading' style='font-size:1.1rem;'>🎭 Emotions Detected</div>
            <div style='display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.8rem;'>
        """, unsafe_allow_html=True)
        
        for emo, emoji in EMOTION_EMOJI.items():
            color = EMOTION_COLORS[emo]
            st.markdown(f"""
            <div style='background:#0d0c20; border:1px solid #2a2050; border-radius:8px; 
                        padding:0.5rem 0.8rem; display:flex; align-items:center; gap:0.5rem;'>
                <span style='font-size:1.1rem;'>{emoji}</span>
                <span style='color:{color}; font-size:0.9rem;'>{emo}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='pm-card' style='margin-top:1rem;'>
            <div class='pm-heading' style='font-size:1.1rem;'>ℹ️ Method</div>
            <p style='color:#b8a8d8; font-size:0.9rem; line-height:1.7;'>
                Uses a curated lexicon of emotional keywords per category. 
                Scores are normalized to show relative presence of each emotion in the text.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Results
    if analyze_btn and poem_input.strip():
        with st.spinner("Analyzing emotional tone..."):
            primary, scores = detect_emotion(poem_input)
        
        st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)
        
        emoji = EMOTION_EMOJI.get(primary, '🎭')
        color = EMOTION_COLORS.get(primary, '#c4a8f5')
        
        st.markdown(f"""
        <div style='text-align:center; padding:1.5rem;'>
            <div style='font-size:3.5rem;'>{emoji}</div>
            <div style='color:#9080b8; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.1em; margin-top:0.5rem;'>Primary Emotion</div>
            <div style='font-family:"Playfair Display",serif; font-size:3rem; font-weight:700; color:{color}; margin:0.2rem 0;'>{primary}</div>
        </div>
        """, unsafe_allow_html=True)
        
        res_col1, res_col2 = st.columns(2, gap="large")
        
        with res_col1:
            # Radar / bar chart
            emotions = list(scores.keys())
            values = [scores[e] * 100 for e in emotions]
            colors_list = [EMOTION_COLORS[e] for e in emotions]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=emotions,
                    y=values,
                    marker_color=colors_list,
                    text=[f"{v:.0f}%" for v in values],
                    textposition='outside',
                    textfont=dict(color='#c4a8f5', size=11),
                )
            ])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(13,12,32,0.8)',
                font=dict(color='#c4a8f5', family='Source Serif 4'),
                xaxis=dict(gridcolor='#2a2050', tickfont=dict(size=11)),
                yaxis=dict(gridcolor='#2a2050', title='Score %', range=[0, max(values)*1.3 + 5]),
                margin=dict(l=20, r=20, t=20, b=20),
                height=300,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with res_col2:
            # Radar chart
            fig2 = go.Figure()
            fig2.add_trace(go.Scatterpolar(
                r=[scores[e] * 100 for e in emotions] + [scores[emotions[0]] * 100],
                theta=emotions + [emotions[0]],
                fill='toself',
                fillcolor='rgba(147, 51, 234, 0.25)',
                line=dict(color='#9333ea', width=2),
                name='Emotion Profile'
            ))
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                polar=dict(
                    bgcolor='rgba(13,12,32,0.8)',
                    radialaxis=dict(visible=True, range=[0, max(values)*1.2 + 5], gridcolor='#2a2050', color='#7060a0'),
                    angularaxis=dict(gridcolor='#2a2050', color='#c4a8f5'),
                ),
                font=dict(color='#c4a8f5', family='Source Serif 4'),
                margin=dict(l=20, r=20, t=20, b=20),
                height=300,
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Poem display
        st.markdown(f"""
        <div>
            <div class='pm-heading' style='font-size:1.1rem;'>Analyzed Poem</div>
            <div class='poem-box'>{poem_input[:600]}{'...' if len(poem_input)>600 else ''}</div>
        </div>
        """, unsafe_allow_html=True)
    
    elif analyze_btn:
        st.warning("Please enter a poem to analyze.")
