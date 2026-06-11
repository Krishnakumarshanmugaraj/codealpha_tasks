import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
INPUT_FILE = "reddit_sentiment_results.csv"
OUTPUT_FILE = "eda_report.png"
print("=" * 50)
print("  CodeAlpha — Task 2: EDA on Reddit r/technology")
print("=" * 50)
df = pd.read_csv(INPUT_FILE)
print("\nSTEP 1: Data Structure")
print(f"  Shape        : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  Columns      : {list(df.columns)}")
print(f"\n  Data Types:\n{df.dtypes.to_string()}")
print("\nSTEP 2: Missing Values")
missing = df.isnull().sum()
print(missing.to_string())
print(f"  Total missing: {missing.sum()}")
print("\nSTEP 3: Basic Statistics")
print(df[["compound_score"]].describe().round(3).to_string())
print("\nSTEP 4: Answering Key Questions")

print("\n  Q1: How many posts per category?")
print(df["category"].value_counts().to_string())

print("\n  Q2: Sentiment distribution?")
print(df["sentiment"].value_counts().to_string())

print("\n  Q3: Average compound score per category?")
print(df.groupby("category")["compound_score"].mean().round(3).to_string())

print("\n  Q4: Average compound score per sentiment?")
print(df.groupby("sentiment")["compound_score"].mean().round(3).to_string())

print("\n  Q5: Any duplicate titles?")
dupes = df["title"].duplicated().sum()
print(f"  Duplicates found: {dupes}")

print("\n  Q6: Longest and shortest titles?")
df["title_length"] = df["title"].apply(lambda x: len(str(x)))
print(f"  Longest  title : {df['title_length'].max()} characters")
print(f"  Shortest title : {df['title_length'].min()} characters")
print(f"  Average  title : {df['title_length'].mean():.1f} characters")
print("\nSTEP 5: Generating EDA Visualizations...")

COLORS = {"Positive": "#2ecc71", "Neutral": "#3498db", "Negative": "#e74c3c"}

fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle("Reddit r/technology — Exploratory Data Analysis",
             fontsize=18, fontweight="bold", y=0.99)
ax = axes[0, 0]
cat_counts = df["category"].value_counts()
bars = ax.bar(cat_counts.index, cat_counts.values,
              color=["#9b59b6", "#e67e22", "#1abc9c"],
              edgecolor="white", width=0.5)
for bar, val in zip(bars, cat_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            str(val), ha="center", fontweight="bold", fontsize=12)
ax.set_title("Posts per Category", fontsize=13, fontweight="bold")
ax.set_xlabel("Category"); ax.set_ylabel("Count")
ax.spines[["top","right"]].set_visible(False)
ax = axes[0, 1]
sent_counts = df["sentiment"].value_counts()
bars = ax.bar(sent_counts.index, sent_counts.values,
              color=[COLORS[s] for s in sent_counts.index],
              edgecolor="white", width=0.5)
for bar, val in zip(bars, sent_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            str(val), ha="center", fontweight="bold", fontsize=12)
ax.set_title("Sentiment Distribution", fontsize=13, fontweight="bold")
ax.set_xlabel("Sentiment"); ax.set_ylabel("Count")
ax.spines[["top","right"]].set_visible(False)
ax = axes[0, 2]
categories = df["category"].unique()
data_to_plot = [df[df["category"] == c]["compound_score"].values for c in categories]
bp = ax.boxplot(data_to_plot, labels=[c.upper() for c in categories],
                patch_artist=True, notch=False)
box_colors = ["#9b59b6", "#e67e22", "#1abc9c"]
for patch, color in zip(bp["boxes"], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.axhline(y=0, color="red", linestyle="--", linewidth=1, alpha=0.5)
ax.set_title("Compound Score by Category", fontsize=13, fontweight="bold")
ax.set_xlabel("Category"); ax.set_ylabel("Compound Score")
ax.spines[["top","right"]].set_visible(False)
ax = axes[1, 0]
ax.hist(df["title_length"], bins=20, color="#3498db", edgecolor="white", alpha=0.8)
ax.axvline(df["title_length"].mean(), color="red", linestyle="--",
           linewidth=1.5, label=f"Mean: {df['title_length'].mean():.1f}")
ax.set_title("Title Length Distribution", fontsize=13, fontweight="bold")
ax.set_xlabel("Number of Characters"); ax.set_ylabel("Frequency")
ax.legend(); ax.spines[["top","right"]].set_visible(False)
ax = axes[1, 1]
sentiments = ["Positive", "Neutral", "Negative"]
data_violin = [df[df["sentiment"] == s]["compound_score"].values for s in sentiments]
vp = ax.violinplot(data_violin, positions=[1, 2, 3], showmedians=True)
for i, (body, color) in enumerate(zip(vp["bodies"], [COLORS[s] for s in sentiments])):
    body.set_facecolor(color)
    body.set_alpha(0.7)
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(sentiments)
ax.set_title("Score Distribution per Sentiment", fontsize=13, fontweight="bold")
ax.set_xlabel("Sentiment"); ax.set_ylabel("Compound Score")
ax.spines[["top","right"]].set_visible(False)
ax = axes[1, 2]
pivot = df.pivot_table(values="compound_score",
                       index="category", columns="sentiment", aggfunc="mean")
sns.heatmap(pivot, annot=True, fmt=".2f", cmap="RdYlGn",
            linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
ax.set_title("Avg Compound Score\n(Category vs Sentiment)", fontsize=13, fontweight="bold")
ax.set_xlabel("Sentiment"); ax.set_ylabel("Category")
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig(OUTPUT_FILE, dpi=150, bbox_inches="tight", facecolor="white")
print(f"  EDA chart saved to: {OUTPUT_FILE}")
plt.show()
print("=" * 50)