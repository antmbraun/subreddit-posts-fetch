from fastapi import FastAPI
from typing import List
import os
import praw
import time

app = FastAPI()

# Reddit API setup from Render environment variables
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

@app.get("/subreddit/{sub}")
def fetch_subreddit_posts(sub: str, limit: int = 1000):
    """Fetch top posts from the past year from the given subreddit."""
    try:
        subreddit = reddit.subreddit(sub)
        posts = []
        for post in subreddit.top(time_filter='year', limit=limit):
            post.comments.replace_more(limit=0)
            top_comments = [c.body.strip() for c in post.comments[:3]]
            posts.append({
                "id": post.id,
                "title": post.title,
                "body": post.selftext,
                "url": post.url,
                "score": post.score,
                "num_comments": post.num_comments,
                "created_utc": post.created_utc,
                "top_comments": top_comments,
                "timestamp": time.strftime('%Y-%m-%d', time.gmtime(post.created_utc))
            })
        return {"subreddit": sub, "count": len(posts), "posts": posts}
    except Exception as e:
        return {"error": str(e)}