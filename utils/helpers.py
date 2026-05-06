import re
import numpy as np
import joblib
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent.parent

def clean_text(text):
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'[^\w\s\n]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text).strip()
    return text

_classifier = None
_form_labels = None
_rec_vectorizer = None
_rec_matrix = None
_rec_poems = None
_markov_chains = None

def load_classifier():
    global _classifier, _form_labels
    if _classifier is None:
        _classifier = joblib.load(BASE / 'models' / 'classifier.pkl')
        _form_labels = joblib.load(BASE / 'models' / 'form_labels.pkl')
    return _classifier, _form_labels

def load_rec_system():
    global _rec_vectorizer, _rec_matrix, _rec_poems
    if _rec_vectorizer is None:
        _rec_vectorizer = joblib.load(BASE / 'models' / 'rec_vectorizer.pkl')
        _rec_matrix = joblib.load(BASE / 'models' / 'rec_matrix.pkl')
        _rec_poems = pd.read_csv(BASE / 'data' / 'rec_poems.csv')
    return _rec_vectorizer, _rec_matrix, _rec_poems

def load_markov():
    global _markov_chains
    if _markov_chains is None:
        _markov_chains = joblib.load(BASE / 'models' / 'markov_chains.pkl')
    return _markov_chains

def predict_form(text):
    clf, labels = load_classifier()
    cleaned = clean_text(text)
    pred = clf.predict([cleaned])[0]
    # Get decision function scores for confidence
    try:
        scores = clf.decision_function([cleaned])[0]
        classes = clf.classes_
        # Softmax-like normalization
        exp_scores = np.exp(scores - scores.max())
        probs = exp_scores / exp_scores.sum()
        top_idx = np.argsort(probs)[::-1][:5]
        top_preds = [(classes[i], float(probs[i])) for i in top_idx]
    except:
        top_preds = [(pred, 1.0)]
    return pred, top_preds

def get_recommendations(text, top_n=5):
    vec, matrix, poems_df = load_rec_system()
    cleaned = clean_text(text)
    query_vec = vec.transform([cleaned])
    from sklearn.metrics.pairwise import cosine_similarity
    sims = cosine_similarity(query_vec, matrix)[0]
    top_idx = np.argsort(sims)[::-1][:top_n+1]
    results = []
    for idx in top_idx:
        score = float(sims[idx])
        if score > 0.01:
            row = poems_df.iloc[idx]
            results.append({
                'poem_text': row['poem_text'],
                'poem_type': row['poem_type'],
                'score': score
            })
    return results[:top_n]

def detect_emotion(text):
    """Rule-based emotion detection using keyword matching."""
    text_lower = text.lower()
    
    emotion_keywords = {
        'Joy': ['happy', 'joy', 'bright', 'smile', 'laugh', 'delight', 'bliss', 'gleam', 'sunshine', 'celebrate', 'merry', 'glad', 'cheer', 'radiant', 'bloom', 'sweet'],
        'Sadness': ['sad', 'grief', 'mourn', 'weep', 'tears', 'sorrow', 'lament', 'despair', 'lonely', 'loss', 'pain', 'ache', 'cry', 'dark', 'shadow', 'lost', 'gone'],
        'Love': ['love', 'heart', 'kiss', 'beloved', 'tender', 'embrace', 'adore', 'romance', 'longing', 'desire', 'passionate', 'devotion', 'cherish', 'dear'],
        'Fear': ['fear', 'dread', 'terror', 'horror', 'tremble', 'dark', 'night', 'shadow', 'haunted', 'ghost', 'doom', 'curse', 'cold', 'alone', 'silence'],
        'Anger': ['rage', 'fury', 'hate', 'anger', 'wrath', 'battle', 'war', 'fight', 'storm', 'thunder', 'burn', 'fire', 'blood', 'strike', 'fierce'],
        'Wonder': ['wonder', 'awe', 'mystery', 'dream', 'sky', 'star', 'infinite', 'eternal', 'magic', 'divine', 'heaven', 'beyond', 'vast', 'silence', 'nature'],
        'Melancholy': ['autumn', 'winter', 'fade', 'wither', 'decay', 'empty', 'hollow', 'pale', 'grey', 'dusk', 'ending', 'passing', 'forgotten', 'still', 'cold'],
    }
    
    scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[emotion] = score
    
    total = sum(scores.values()) or 1
    probs = {e: round(s / total, 3) for e, s in scores.items()}
    primary = max(probs, key=probs.get)
    
    return primary, probs

def generate_poem(style='general', theme='', num_lines=10):
    import random
    chains = load_markov()
    
    chain = chains.get(style, chains.get('general', {}))
    if not chain:
        return "The stars in silence fall..."
    
    # Find a seed word matching theme
    seed = None
    if theme:
        seed_candidates = [k for k in chain.keys() if theme.lower() in ' '.join(k)]
        if seed_candidates:
            seed = random.choice(seed_candidates)
    
    if not seed:
        seed = random.choice(list(chain.keys()))
    
    result_words = list(seed)
    current = seed
    target = num_lines * 7
    
    for _ in range(target + 20):
        if current in chain and chain[current]:
            next_word = random.choice(chain[current])
            result_words.append(next_word)
            current = tuple(result_words[-2:])
        else:
            if chain:
                current = random.choice(list(chain.keys()))
                result_words.extend(list(current))
    
    # Format into lines with varying length for poetry feel
    lines = []
    i = 0
    line_lengths = [6, 8, 5, 9, 7, 6, 8, 5, 7, 9]
    ln_idx = 0
    while i < len(result_words) and len(lines) < num_lines:
        ll = line_lengths[ln_idx % len(line_lengths)]
        chunk = result_words[i:i+ll]
        if chunk:
            line = ' '.join(chunk).capitalize()
            lines.append(line)
            i += ll
            ln_idx += 1
    
    return '\n'.join(lines)
