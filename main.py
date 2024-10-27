from fastapi import FastAPI, HTTPException
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

def get_subfeddit_id(subfeddit_name):
    api_url = 'http://feddit:8080/api/v1/subfeddits/?skip=0&limit=10'

    try:
        response = requests.get(api_url)

        response.raise_for_status()
        data = response.json()
        
        # Find subfeddit by name
        subfeddits = data.get('subfeddits', [])
        for subfeddit in subfeddits:
            if subfeddit.get('title', '') == subfeddit_name:
                return subfeddit.get("id", '')

        # Raise exception if subfeddit is not found
        raise HTTPException(status_code=404, detail="Subfeddit not found")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve subfeddit ID")


@app.get("/")
def index():
    return {"details": "Hello World!"}

@app.get("/comments", response_model=CommentResponse)
async def get_latest_comments(
        subfeddit_name: str,
        start_date: datetime = None,
        end_date: datetime = None,
        sort_by_polarity: bool = False
    ):
    """
    Fetches and processes comments from a specified subfeddit.

    Parameters:
    - subfeddit_id: ID of the subfeddit to fetch comments from
    - start_date: Filter to include comments only after this date
    - end_date: Filter to include comments only before this date
    - sort_by_polarity: Optionally sort comments by polarity score in descending order

    Returns:
    - A JSON response containing the latest 25 comments from a specific subfeddit
    """
    limit=25
    comments_per_page=100
    all_comments = []
    skip = 0

    subfeddit_id = get_subfeddit_id(subfeddit_name)

    while True:
        api_url = f'http://feddit:8080/api/v1/comments/?subfeddit_id={subfeddit_id}&skip={skip}&limit={comments_per_page}'

        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()

            # Parse JSON response and extend comments list
            data = response.json()
            comments = data.get('comments', [])
            all_comments.extend(comments)

            # Exit if fewer comments than requested were received
            if len(comments) < comments_per_page:
                break

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail="Failed to retrieve comments")


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