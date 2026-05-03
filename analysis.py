import pandas as pd
import re
from collections import Counter
from textblob import TextBlob

# Clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

# Theme dictionary (Grounded Theory approach)
themes_dict = {
    "salary": ["salary", "pay", "income"],
    "work_life": ["balance", "hours", "overtime", "pressure"],
    "management": ["manager", "boss", "management"],
    "growth": ["growth", "career", "learning", "promotion"],
    "environment": ["team", "culture", "environment"]
}

# Assign themes
def assign_theme(text):
    found = []
    for theme, words in themes_dict.items():
        for word in words:
            if word in text:
                found.append(theme)
    return list(set(found))

# Sentiment analysis
def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Main processing
def analyze_data(df):
    df['cleaned'] = df['feedback'].apply(clean_text)
    df['themes'] = df['cleaned'].apply(assign_theme)
    df['sentiment'] = df['feedback'].apply(get_sentiment)

    all_themes = sum(df['themes'], [])
    theme_count = Counter(all_themes)

    sentiment_count = df['sentiment'].value_counts()

    return df, theme_count, sentiment_count