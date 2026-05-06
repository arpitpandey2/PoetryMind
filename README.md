# 🖋️ PoetryMind — AI-Based Poetry Analysis & Generation Platform

A full-stack machine learning platform for poetry analysis, classification, recommendation, and generation.

## 📁 Project Structure

```
PoetryMind/
├── app.py                  # Main Streamlit entry point
├── requirements.txt
├── data/
│   ├── master.csv          # 20,487 poems with metadata
│   ├── rec_poems.csv       # 2,000 poems for recommendation
│   └── analytics.json      # Precomputed analytics
├── models/
│   ├── classifier.pkl      # LinearSVC poem form classifier
│   ├── form_labels.pkl     # Form label list
│   ├── rec_vectorizer.pkl  # TF-IDF vectorizer for recommendations
│   ├── rec_matrix.pkl      # TF-IDF matrix for cosine similarity
│   └── markov_chains.pkl   # Markov chains per poetic form
├── pages/
│   ├── home.py             # Home / landing page
│   ├── classifier.py       # Poem form classification
│   ├── emotion.py          # Emotion detection
│   ├── generator.py        # AI poem generation
│   ├── recommendations.py  # Similar poem finder
│   └── analytics.py        # Dataset analytics dashboard
└── utils/
    └── helpers.py          # Shared ML utilities
```

## 🚀 Running the App

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🧠 ML Models

| Model | Algorithm | Purpose |
|-------|-----------|---------|
| Form Classifier | LinearSVC + TF-IDF | Predict poetic form (sonnet, ballad, haiku, etc.) |
| Recommender | Cosine Similarity | Find similar poems |
| Generator | Markov Chains (bigram) | Generate original poems |
| Emotion Detector | Keyword Lexicon | Detect joy, sadness, love, fear, anger, wonder, melancholy |

## 📊 Dataset

- **Source**: Scraped poetry corpus
- **Size**: 20,487 poems
- **Forms**: 136 poetic forms (villanelle, sonnet, ballad, haiku, etc.)
- **Topics**: 144 thematic categories (love, war, nature, death, etc.)

## 🎓 Concepts Covered

- NLP preprocessing (TF-IDF, bigrams)
- Supervised text classification (LinearSVC)
- Unsupervised similarity (cosine similarity)
- Text generation (Markov chains)
- Data visualization (Plotly)
- Full-stack web deployment (Streamlit)

## 🌐 Deployment

Deploy to Streamlit Cloud:
1. Push to GitHub
2. Go to share.streamlit.io
3. Connect your repo
4. Set main file as `app.py`
