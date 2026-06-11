# CodeAlpha

## Project: Reddit r/technology — Sentiment Analysis & Data Insights

## Overview

This project was completed as part of the **CodeAlpha Data Analytics Internship**.
It involves scraping real-time data from Reddit's r/technology subreddit,
performing exploratory data analysis, sentiment analysis, and building
a comprehensive data visualization dashboard.

---

## Tasks Completed

### Task 1: Web Scraping
- Scraped posts from Reddit's r/technology subreddit (Hot, New, Top categories)
- Used BeautifulSoup to parse Reddit's public RSS feed
- Collected 81 unique posts with title, author, date, score, and comments
- Saved dataset as `reddit_technology_posts.csv`

### Task 2: Exploratory Data Analysis (EDA)
- Explored data structure, shape, columns, and data types
- Identified missing values, duplicates, and anomalies
- Answered 6 meaningful questions about the dataset
- Analyzed title length, category distribution, and score patterns
- Generated 6 EDA charts saved as `eda_report.png`

### Task 3: Data Visualization
- Built a 6-chart sentiment analysis dashboard
- Used Matplotlib, Seaborn, and WordCloud for visualizations
- Charts include: Pie chart, Bar chart, Histogram, Grouped bar, Horizontal bar, Word cloud
- Dashboard saved as `reddit_sentiment_dashboard.png`

### Task 4: Sentiment Analysis
- Analyzed all post titles using VADER Sentiment Analysis
- Classified each post as Positive, Neutral, or Negative
- Results: 30 Negative | 29 Neutral | 22 Positive
- Average compound score: -0.057 (r/technology leans slightly negative)
- Saved results as `reddit_sentiment_results.csv`

---

## Project Workflow

```
Reddit r/technology Website
         |  (Task 1: scraping.py)
         v
reddit_technology_posts.csv
         |  (Task 4: sentiment_analysis.py)
         v
reddit_sentiment_results.csv
         |  (Task 2: eda.py)
         v
eda_report.png
         |  (Task 3: visualization.py)
         v
reddit_sentiment_dashboard.png
```

---

## Tools and Libraries Used

| Library        | Purpose                            |
|----------------|------------------------------------|
| requests       | Sending HTTP requests to Reddit    |
| BeautifulSoup  | Parsing HTML/XML structure         |
| pandas         | Data manipulation and analysis     |
| vaderSentiment | Sentiment classification           |
| matplotlib     | Chart and graph generation         |
| seaborn        | Statistical visualizations         |
| wordcloud      | Word frequency visualization       |

---

## Dataset Details

- **Source:** Reddit r/technology (www.reddit.com/r/technology)
- **Method:** RSS Feed scraping using BeautifulSoup
- **Total Posts:** 81 unique posts
- **Categories:** Hot, New, Top
- **Fields:** title, author, published, link, score, num_comments, category, content, compound_score, sentiment

---

## Key Findings

- r/technology posts lean slightly negative overall (average compound score: -0.057)
- 37% of posts are Negative — tech news frequently covers data breaches, legal cases, and privacy issues
- 27% of posts are Positive — driven by new product launches and research breakthroughs
- Most frequently occurring words: AI, Google, Apple, data, privacy, new

---

## How to Run

**Step 1: Install dependencies**
```bash
pip install requests beautifulsoup4 lxml pandas matplotlib seaborn wordcloud vaderSentiment
```

**Step 2: Run scripts in the following order**
```bash
python scraping.py
python sentiment_analysis.py
python eda.py
python visualization.py
```

---

## Output Files

| File                              | Description                        |
|-----------------------------------|------------------------------------|
| reddit_technology_posts.csv       | Raw scraped dataset                |
| reddit_sentiment_results.csv      | Dataset with sentiment labels      |
| eda_report.png                    | EDA visualization dashboard        |
| reddit_sentiment_dashboard.png    | Sentiment analysis dashboard       |

---

## Author

- **Internship:** CodeAlpha Data Analytics Internship
- **Company:** CodeAlpha (www.codealpha.tech)
