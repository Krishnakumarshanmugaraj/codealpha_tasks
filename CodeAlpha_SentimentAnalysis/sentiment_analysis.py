import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import os

INPUT_FILE  = "reddit_technology_posts.csv"
OUTPUT_FILE = "reddit_sentiment_results.csv"
print("Loading data...")
df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} posts")
print(f"Columns: {list(df.columns)}\n")
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    if not isinstance(text, str) or text.strip() == "":
        return 0.0, "Neutral"
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return compound, label

print("Running sentiment analysis on titles...")
df[["compound_score", "sentiment"]] = df["title"].apply(
    lambda t: pd.Series(get_sentiment(t))
)
print("\n=== Sentiment Summary ===")
counts = df["sentiment"].value_counts()
print(counts.to_string())
print(f"\nAverage compound score: {df['compound_score'].mean():.3f}")
print("\nMost Positive Posts:")
print(df.nlargest(3, "compound_score")[["title","compound_score"]].to_string(index=False))
print("\nMost Negative Posts:")
print(df.nsmallest(3, "compound_score")[["title","compound_score"]].to_string(index=False))
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
print(f"\nResults saved to: {OUTPUT_FILE}")
print("\nDone!")