import requests
from textblob import TextBlob
import json
from datetime import datetime

def get_polarity_score(comment):
    return TextBlob(comment).sentiment.polarity

def compute_sentiment(polarity_score):
    if polarity_score >= 0:
        return 'Positive'
    else:
        return 'Negative'

def get_subfeddits():
    URL = 'http://0.0.0.0:8080/api/v1/subfeddits/?skip=0&limit=1'
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        print(print(json.dumps(data, indent=4)))
    else:
        print('Error')

def get_subfeddit(subfeddit_id):
    URL = f'http://0.0.0.0:8080/api/v1/subfeddit/?subfeddit_id={subfeddit_id}'
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        for comment in data["comments"]:
            timestamp = comment["created_at"]
            # Convert Unix timestamp to datetime in a readable format
            comment["created_at"] = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        print(print(json.dumps(data, indent=4)))
    else:
        print('Error')

def get_comments():
    limit = 50000
    skip = 0
    FEDDIT_API_URL = f'http://0.0.0.0:8080/api/v1/comments/?subfeddit_id=2&skip={skip}&limit={limit}'
    response = requests.get(FEDDIT_API_URL)

    if response.status_code == 200:
        data = response.json()

        for comment in data["comments"]:
            timestamp = comment["created_at"]
            # Convert Unix timestamp to datetime in a readable format
            comment["created_at"] = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        #print(json.dumps(data, indent=4))

    else:
        print('Error')

def get_latest_comments(subfeddit_id, limit=25, comments_per_page=50000):

    all_comments = []
    skip = 0
    i = 0
    unique_ids = []
    while True:
        api_url = f'http://0.0.0.0:8080/api/v1/comments/?subfeddit_id={subfeddit_id}&skip={skip}&limit={comments_per_page}'
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            comments = data.get('comments', [])
            all_comments.extend(comments)
            print("Retrieved " + str(len(comments)) + " comments")
            print("skip: " + str(skip))
            for comment in comments:
                if comment["id"] not in unique_ids:
                    unique_ids.append(comment["id"])
                else:
                    print(str(comment["id"]) + "already present")

            # Check if we received fewer comments than requested
            if len(comments) < comments_per_page:
                break  
            
            skip += comments_per_page
        else:
            print("Error fetching comments:", response.status_code, response.text)
            break
    
    print("unique ids: " + str(len(unique_ids)))
    sorted_comments = sorted(all_comments, key=lambda x: x['created_at'], reverse=True)
    #(json.dumps(sorted_comments, indent=4))
    latest_comments = sorted_comments[:limit]
    
    return latest_comments



if __name__ == '__main__':
    
    latest_comments = get_latest_comments(2)
    
    for comment in latest_comments:
            timestamp = comment["created_at"]
            # Convert Unix timestamp to datetime in a readable format
            comment["created_at"] = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            polarity_score = get_polarity_score(comment["text"])
            comment["polarity_score"] = polarity_score
            comment["sentiment"] = compute_sentiment(polarity_score)

    #get_comments()
    print("-------------------------------------------------")
    print(json.dumps(latest_comments, indent=4))
    

