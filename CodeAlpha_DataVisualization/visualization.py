import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from wordcloud import WordCloud
import warnings
warnings.filterwarnings("ignore")
INPUT_FILE = "reddit_sentiment_results.csv"
print("Loading data...")
df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} posts\n")
COLORS = {
    "Positive": "#2ecc71",
    "Neutral":  "#3498db",
    "Negative": "#e74c3c"
}
fig = plt.figure(figsize=(18, 14))
fig.suptitle("Reddit r/technology — Sentiment Analysis Dashboard",
             fontsize=20, fontweight="bold", y=0.98)
ax1 = fig.add_subplot(2, 3, 1)
counts = df["sentiment"].value_counts()
colors = [COLORS[s] for s in counts.index]
wedges, texts, autotexts = ax1.pie(
    counts.values,
    labels=counts.index,
    autopct="%1.1f%%",
    colors=colors,
    startangle=140,
    textprops={"fontsize": 11}
)
for at in autotexts:
    at.set_fontweight("bold")
ax1.set_title("Sentiment Distribution", fontsize=13, fontweight="bold", pad=15)
ax2 = fig.add_subplot(2, 3, 2)
bars = ax2.bar(counts.index, counts.values,
               color=[COLORS[s] for s in counts.index],
               edgecolor="white", linewidth=1.5, width=0.5)
for bar, val in zip(bars, counts.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             str(val), ha="center", va="bottom", fontweight="bold", fontsize=12)
ax2.set_title("Post Count by Sentiment", fontsize=13, fontweight="bold")
ax2.set_xlabel("Sentiment", fontsize=11)
ax2.set_ylabel("Number of Posts", fontsize=11)
ax2.set_ylim(0, counts.max() + 6)
ax2.spines[["top", "right"]].set_visible(False)
ax3 = fig.add_subplot(2, 3, 3)
ax3.hist(df[df["sentiment"] == "Positive"]["compound_score"],
         bins=12, color=COLORS["Positive"], alpha=0.7, label="Positive")
ax3.hist(df[df["sentiment"] == "Neutral"]["compound_score"],
         bins=12, color=COLORS["Neutral"], alpha=0.7, label="Neutral")
ax3.hist(df[df["sentiment"] == "Negative"]["compound_score"],
         bins=12, color=COLORS["Negative"], alpha=0.7, label="Negative")
ax3.axvline(x=0.05,  color="gray", linestyle="--", linewidth=1, alpha=0.7)
ax3.axvline(x=-0.05, color="gray", linestyle="--", linewidth=1, alpha=0.7)
ax3.set_title("Compound Score Distribution", fontsize=13, fontweight="bold")
ax3.set_xlabel("Compound Score", fontsize=11)
ax3.set_ylabel("Frequency", fontsize=11)
ax3.legend(fontsize=10)
ax3.spines[["top", "right"]].set_visible(False)
ax4 = fig.add_subplot(2, 3, 4)
cat_sent = df.groupby(["category", "sentiment"]).size().unstack(fill_value=0)
cat_sent = cat_sent.reindex(columns=["Positive", "Neutral", "Negative"])
x = range(len(cat_sent.index))
width = 0.25
for i, sentiment in enumerate(["Positive", "Neutral", "Negative"]):
    if sentiment in cat_sent.columns:
        bars = ax4.bar([xi + i*width for xi in x],
                       cat_sent[sentiment],
                       width=width,
                       color=COLORS[sentiment],
                       label=sentiment,
                       edgecolor="white")
ax4.set_xticks([xi + width for xi in x])
ax4.set_xticklabels([c.upper() for c in cat_sent.index], fontsize=11)
ax4.set_title("Sentiment by Category", fontsize=13, fontweight="bold")
ax4.set_xlabel("Category", fontsize=11)
ax4.set_ylabel("Number of Posts", fontsize=11)
ax4.legend(fontsize=10)
ax4.spines[["top", "right"]].set_visible(False)
ax5 = fig.add_subplot(2, 3, 5)
top_df = pd.concat([
    df.nlargest(5, "compound_score"),
    df.nsmallest(5, "compound_score")
]).drop_duplicates()
top_df = top_df.sort_values("compound_score")
short_titles = [t[:45] + "..." if len(t) > 45 else t for t in top_df["title"]]
bar_colors = [COLORS[s] for s in top_df["sentiment"]]
bars = ax5.barh(range(len(top_df)), top_df["compound_score"],
                color=bar_colors, edgecolor="white")
ax5.set_yticks(range(len(top_df)))
ax5.set_yticklabels(short_titles, fontsize=8)
ax5.axvline(x=0, color="black", linewidth=0.8)
ax5.set_title("Top 5 Positive & Negative Posts", fontsize=13, fontweight="bold")
ax5.set_xlabel("Compound Score", fontsize=11)
ax5.spines[["top", "right"]].set_visible(False)
patches = [mpatches.Patch(color=COLORS[s], label=s) for s in ["Positive", "Neutral", "Negative"]]
ax5.legend(handles=patches, fontsize=9, loc="lower right")
ax6 = fig.add_subplot(2, 3, 6)
all_titles = " ".join(df["title"].dropna().tolist())
stopwords = {"the","a","an","in","of","to","and","is","for","on",
             "with","at","by","from","that","this","it","as","are","be"}
wordcloud = WordCloud(
    width=500, height=300,
    background_color="white",
    stopwords=stopwords,
    colormap="RdYlGn",
    max_words=60
).generate(all_titles)
ax6.imshow(wordcloud, interpolation="bilinear")
ax6.axis("off")
ax6.set_title("Most Common Words in Titles", fontsize=13, fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("reddit_sentiment_dashboard.png", dpi=150,
            bbox_inches="tight", facecolor="white")
print("Dashboard saved to: reddit_sentiment_dashboard.png")
plt.show()
print("\nDone!")