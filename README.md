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
