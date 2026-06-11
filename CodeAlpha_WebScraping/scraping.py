import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

OUTPUT_FILE = "reddit_technology_posts.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

FEEDS = [
    ("hot",  "https://www.reddit.com/r/technology/hot/.rss?limit=50"),
    ("new",  "https://www.reddit.com/r/technology/new/.rss?limit=50"),
    ("top",  "https://www.reddit.com/r/technology/top/.rss?limit=50"),
]

def scrape_feed(category, url):
    print(f"  Fetching {category} feed...")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        print(f"  Status: {r.status_code}")
        if r.status_code != 200:
            print(f"  Skipping {category}")
            return []

        soup = BeautifulSoup(r.content, "xml")
        entries = soup.find_all("entry")
        print(f"  Posts found: {len(entries)}")

        results = []
        for entry in entries:
            title     = entry.find("title").get_text(strip=True) if entry.find("title") else ""
            link      = entry.find("link")["href"] if entry.find("link") else ""
            author    = entry.find("author").get_text(strip=True) if entry.find("author") else ""
            published = entry.find("published").get_text(strip=True) if entry.find("published") else ""
            content   = entry.find("content").get_text(strip=True) if entry.find("content") else ""
            score = 0
            comments = 0
            for line in content.split("\n"):
                if "score" in line.lower():
                    try: score = int(''.join(filter(str.isdigit, line)))
                    except: pass
                if "comment" in line.lower():
                    try: comments = int(''.join(filter(str.isdigit, line)))
                    except: pass

            results.append({
                "title":        title,
                "author":       author,
                "published":    published,
                "link":         link,
                "score":        score,
                "num_comments": comments,
                "category":     category,
                "content":      content[:300],  
            })
        return results

    except Exception as e:
        print(f"  Error: {e}")
        return []

def main():
    print("\nReddit RSS Scraper — r/technology")
    print("=" * 45)

    all_posts = []
    for category, url in FEEDS:
        posts = scrape_feed(category, url)
        all_posts.extend(posts)
        time.sleep(2)

    if not all_posts:
        print("\nNo data scraped.")
        return None
    df = pd.DataFrame(all_posts)
    df = df.drop_duplicates(subset="link")
    print(f"\nTotal posts scraped : {len(df)}")
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"Data saved to      : {OUTPUT_FILE}")
    print("\nSample:")
    print("-" * 45)
    print(df[["title", "score", "num_comments", "category"]].head(5).to_string(index=False))
    print("\nDone!")
    return df
if __name__ == "__main__":
    df = main()