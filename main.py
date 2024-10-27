from fastapi import FastAPI
import requests
from textblob import TextBlob
import json
from datetime import datetime
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Comment(BaseModel):
    id: str
    username: str
    text: str
    created_at: datetime
    polarity_score: float
    sentiment: str

class CommentResponse(BaseModel):
    comments: List[Comment]

def get_polarity_score(comment):
    return TextBlob(comment).sentiment.polarity

def compute_sentiment(polarity_score):
    if polarity_score >= 0:
        return 'Positive'
    else:
        return 'Negative'

@app.get("/")
def index():
    return {"details": "Hello World!"}

@app.get("/comments", response_model=CommentResponse)
async def get_latest_comments(
        subfeddit_id: str,
        start_date: datetime = None,
        end_date: datetime = None,
        sort_by_polarity: bool = False
    ):
    limit=25
    comments_per_page=100
    all_comments = []
    skip = 0

    while True:
        api_url = f'http://feddit:8080/api/v1/comments/?subfeddit_id={subfeddit_id}&skip={skip}&limit={comments_per_page}'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            comments = data.get('comments', [])
            all_comments.extend(comments)

            # Check if we received fewer comments than requested
            if len(comments) < comments_per_page:
                break  
        else:
            print("Error fetching comments:", response.status_code, response.text)
            break

        skip += comments_per_page

    latest_comments = all_comments[::-1][:limit]

    # Filter comments by date if start_date and/or end_date are provided
    filtered_comments = []
    for comment in latest_comments:
        timestamp = comment["created_at"]
        comment_datetime = datetime.utcfromtimestamp(timestamp)
        
        # Apply date filters if set
        if start_date and comment_datetime < start_date:
            continue
        if end_date and comment_datetime > end_date:
            continue

        # Calculate polarity score and determine sentiment
        polarity_score = get_polarity_score(comment["text"])
        sentiment = compute_sentiment(polarity_score)

        processed_comment = Comment(
            id=str(comment["id"]),
            username=comment["username"],
            text=comment["text"],
            created_at=comment_datetime,
            polarity_score=polarity_score,
            sentiment=sentiment
        )
        filtered_comments.append(processed_comment)

    # Sort by polarity if requested
    if sort_by_polarity:
        filtered_comments.sort(key=lambda x: x.polarity_score, reverse=True)

    # Return the filtered and processed comments in the response model format
    return {"comments": filtered_comments}