import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import json
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent.parent

PLOT_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13,12,32,0.8)',
    font=dict(color='#c4a8f5', family='Source Serif 4', size=11),
    margin=dict(l=20, r=20, t=30, b=20),
)

def render():
    st.markdown("""
    <div style='padding:1.5rem 0 1rem 0;'>
        <div class='pm-title' style='font-size:2.5rem;'>📊 Analytics <span style='color:#9333ea;'>Dashboard</span></div>
        <div class='pm-subtitle'>Explore the PoetryMind corpus with interactive charts</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)

    # Load analytics
    with open(BASE / 'data' / 'analytics.json') as f:
        analytics = json.load(f)
    
    # Top metrics
    st.markdown(f"""
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
            <div class='metric-val'>6,214</div>
            <div class='metric-label'>Form Poems</div>
        </div>
        <div class='metric-box'>
            <div class='metric-val'>14,273</div>
            <div class='metric-label'>Topic Poems</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📖 Forms Distribution", "🏷️ Topics Distribution", "💬 Word Frequency"])
    
    with tab1:
        top_forms = analytics['top_forms']
        forms = list(top_forms.keys())
        counts = list(top_forms.values())
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("<div class='pm-heading' style='font-size:1.1rem;'>Top 15 Poem Forms (Bar)</div>", unsafe_allow_html=True)
            colors = px.colors.sequential.Purples[2:][::-1] * 4
            fig = go.Figure(go.Bar(
                x=counts,
                y=[f.replace('-',' ').title() for f in forms],
                orientation='h',
                marker_color=colors[:len(forms)],
                text=counts,
                textposition='outside',
                textfont=dict(color='#c4a8f5', size=10),
            ))
            fig.update_layout(
                **PLOT_THEME,
                height=420,
                xaxis=dict(gridcolor='#2a2050', title='Number of Poems'),
                yaxis=dict(gridcolor='#2a2050', autorange='reversed'),
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<div class='pm-heading' style='font-size:1.1rem;'>Top 15 Forms (Donut)</div>", unsafe_allow_html=True)
            fig2 = go.Figure(go.Pie(
                labels=[f.replace('-',' ').title() for f in forms],
                values=counts,
                hole=0.5,
                marker_colors=px.colors.sequential.Purples[1:][::-1] * 2,
                textinfo='label+percent',
                textfont=dict(size=9, color='white'),
            ))
            fig2.update_layout(
                **PLOT_THEME,
                height=420,
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Avg length chart
        st.markdown("<div class='pm-heading' style='font-size:1.1rem; margin-top:1rem;'>Average Poem Length by Form (chars)</div>", unsafe_allow_html=True)
        avg_len = analytics.get('avg_length_by_form', {})
        if avg_len:
            sorted_avg = dict(sorted(avg_len.items(), key=lambda x: x[1], reverse=True))
            fig3 = go.Figure(go.Bar(
                x=[k.replace('-',' ').title() for k in sorted_avg.keys()],
                y=list(sorted_avg.values()),
                marker_color='#6b46c1',
                marker_line_color='#9333ea',
                marker_line_width=1,
            ))
            fig3.update_layout(
                **PLOT_THEME,
                height=280,
                xaxis=dict(gridcolor='#2a2050', tickangle=-30),
                yaxis=dict(gridcolor='#2a2050', title='Avg Characters'),
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        top_topics = analytics['top_topics']
        topics = list(top_topics.keys())
        tcounts = list(top_topics.values())
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("<div class='pm-heading' style='font-size:1.1rem;'>Top 15 Topics (Bar)</div>", unsafe_allow_html=True)
            topic_colors = px.colors.sequential.Teal[2:][::-1] * 4
            fig4 = go.Figure(go.Bar(
                x=tcounts,
                y=[t.title() for t in topics],
                orientation='h',
                marker_color=topic_colors[:len(topics)],
                text=tcounts,
                textposition='outside',
                textfont=dict(color='#80d8d0', size=10),
            ))
            fig4.update_layout(
                **PLOT_THEME,
                height=420,
                xaxis=dict(gridcolor='#2a2050', title='Number of Poems'),
                yaxis=dict(gridcolor='#2a2050', autorange='reversed'),
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        with col2:
            st.markdown("<div class='pm-heading' style='font-size:1.1rem;'>Topics Treemap</div>", unsafe_allow_html=True)
            fig5 = go.Figure(go.Treemap(
                labels=[t.title() for t in topics],
                parents=[''] * len(topics),
                values=tcounts,
                marker_colorscale='Teal',
                textfont=dict(size=12, color='white'),
            ))
            fig5.update_layout(
                **PLOT_THEME,
                height=420,
            )
            st.plotly_chart(fig5, use_container_width=True)
    
    with tab3:
        st.markdown("<div class='pm-heading' style='font-size:1.1rem;'>Top 50 Most Frequent Words</div>", unsafe_allow_html=True)
        top_words = analytics.get('top_words', {})
        if top_words:
            words_list = list(top_words.keys())[:30]
            word_counts = [top_words[w] for w in words_list]
            
            # Color by frequency
            max_count = max(word_counts)
            norm_counts = [c/max_count for c in word_counts]
            bar_colors = [f'rgba({int(107 + 100*n)}, {int(70 + 50*n)}, {int(193 + 50*(1-n))}, 0.9)' 
                         for n in norm_counts]
            
            fig6 = go.Figure(go.Bar(
                x=words_list,
                y=word_counts,
                marker_color=bar_colors,
                text=word_counts,
                textposition='outside',
                textfont=dict(color='#c4a8f5', size=9),
            ))
            fig6.update_layout(
                **PLOT_THEME,
                height=350,
                xaxis=dict(gridcolor='#2a2050', tickangle=-30),
                yaxis=dict(gridcolor='#2a2050', title='Frequency'),
            )
            st.plotly_chart(fig6, use_container_width=True)
            
            # Word table
            st.markdown("<div class='pm-heading' style='font-size:1.1rem; margin-top:0.5rem;'>Full Word Frequency Table</div>", unsafe_allow_html=True)
            wdf = pd.DataFrame({'Word': list(top_words.keys()), 'Frequency': list(top_words.values())})
            st.dataframe(
                wdf,
                use_container_width=True,
                height=250,
                hide_index=True,
            )
    
    st.markdown("<hr class='pm-divider'>", unsafe_allow_html=True)
    
    # Dataset summary
    st.markdown("""
    <div class='pm-card'>
        <div class='pm-heading' style='font-size:1.2rem;'>🗂️ Dataset Summary</div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin-top:1rem;'>
            <div>
                <div style='color:#9080b8; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>Corpus Organization</div>
                <div style='color:#c4a8f5; font-size:0.9rem; line-height:1.9;'>
                    • <strong>Forms dataset:</strong> 136 directories of poetic forms<br>
                    • <strong>Topics dataset:</strong> 144 directories by theme<br>
                    • Each poem stored as individual .txt file<br>
                    • Average poem: ~800 characters<br>
                    • Range: haiku (3 lines) to epic ballads (100+ lines)
                </div>
            </div>
            <div>
                <div style='color:#9080b8; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>ML Models Built</div>
                <div style='color:#c4a8f5; font-size:0.9rem; line-height:1.9;'>
                    • <strong>Classifier:</strong> LinearSVC + TF-IDF (57% acc)<br>
                    • <strong>Recommender:</strong> Cosine similarity on 2,000 poems<br>
                    • <strong>Generator:</strong> Markov chains for 8 form types<br>
                    • <strong>Emotion:</strong> Keyword lexicon, 7 categories<br>
                    • <strong>Features:</strong> Bigrams, 10K TF-IDF vocabulary
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
