# ML-Engineering-Challenge

## Introduction
This repository contains the code for the ML Engineering challenge utilizing the Feddit API, a mock API designed for retrieving comments from subfeddits. The objective of the challenge was to create a microservice application that provides a RESTful API for classifying comments as either positive or negative based on their sentiment within a specified subfeddit or category.

To accomplish this, I used FastAPI as the framework for developing the API endpoints. Additionally, to facilitate deployment and runtime management, the microservice has been encapsulated within a Docker container, ensuring an efficient and flexible deployment process.

## How-to-run
1. Please make sure you have docker installed.
2. In order to run the microservice, replace `<path-to-docker-compose.yml>` by the actual path of the given `docker-compose.yml` file in `docker compose -f <path-to-docker-compose.yml> up -d`. It should be available in [http://0.0.0.0:8000](http://0.0.0.0:8000).
3. To stop the microservice,  replace `<path-to-docker-compose.yml>` by the actual path of the given `docker-compose.yml` file in `docker compose -f <path-to-docker-compose.yml> down`.

## API Description
This Python file implements a microservice using FastAPI that interacts with the Feddit API to retrieve and analyze comments from specified subfeddits. The service is designed to classify comments as either positive or negative based on their sentiment.

**Key Features**
- FastAPI Framework: The application utilizes FastAPI to create a RESTful API
- Comment Model: The Comment class, defined using Pydantic, structures the comment data, including fields for ID, username, text, creation date, polarity score, and sentiment classification.
- Sentiment Analysis: The service employs the TextBlob library to calculate the polarity score of comments, which is used to determine whether the sentiment is positive or negative.
- Subfeddit Retrieval: A dedicated function retrieves the ID of a subfeddit by its name from the Feddit API. If the subfeddit is not found or an error occurs during the request, appropriate HTTP exceptions are raised.
- Comments Endpoint: The /comments endpoint fetches the latest comments from a specified subfeddit, with options to filter by date and sort by polarity. It returns the latest 25 comments along with their computed sentiment.

## API Parameters
The GET /comments endpoint in this FastAPI-based microservice allows you to retrieve and analyze comments from a specific "subfeddit." The parameters allow filtering by date and sorting based on sentiment polarity. Below is an explanation of the expected parameters:

**Request Parameters**
- `subfeddit_name (required, str)`:
The name of the subfeddit from which to retrieve comments.
- `start_date (optional, datetime)`:
Filters comments to only include those created after this date.
Date should be provided in ISO 8601 format (e.g., 2023-08-01T00:00:00).
- `end_date (optional, datetime)`:
Filters comments to only include those created before this date.
Date should also be in ISO 8601 format.
- `sort_by_polarity (optional, bool)`:
When true, comments are sorted by their polarity score in descending order (from most positive to most negative).
Default is false, which returns comments in the order they were retrieved.

**Response Structure**
The API response includes a JSON object with a list of comments. Each comment contains the following fields:
- `id (str)`: Unique identifier of the comment.
- `username (str)`: Username of the commenter.
- `text (str)`: Content of the comment.
- `created_at (datetime)`: Datetime when the comment was created.
- `polarity_score (float)`: Polarity score of the comment text (range: -1.0 to 1.0).
- `sentiment (str)`: The sentiment analysis result (Positive or Negative), based on the polarity score.

## Github Workflows
A workflow has been configured to run linting with the flake8 library, the .flake8 file contains some configurations to exclude files (like the virtual environment) from the linting process and it also excludes some rule codes related to spacing inside the python files.
