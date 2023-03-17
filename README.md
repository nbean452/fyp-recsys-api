# About

This is the API server of my Final Year Project for Course Recommender System. Keep in mind that this project is still in progress!

This application provides Content-Based Filtering (CBF) and Collaborative Filtering (CF) Recommendations.

For CBF recommender system, I'm using `Term Frequency - Inverse Document Frequency (TF-IDF)` to vectorize corpus of PolyU's computing subject descriptions and `Cosine Similarity` helps find the degree of similarity for these courses.

For CF recommender system, I'll be gathering user reviews about each course and using `Alternating Least Square (ALS)` technique to train the Machine Learning model. The Django server generates new machine learning model every 30 minutes.

Made using [Django](https://www.djangoproject.com/).

## Deployment

Deployed as a dockerized app alongside Next.js app within Digital Ocean's droplet.

Deployment link [here](https://capstone-api.nbenedictcodes.com)

## Q: Where is the Machine Learning code?

Go to `recommendations/mixins.py` and `recomendations/cron.py` and feel free to take a look at each respective Content-Based Filtering and Collaborative Filtering recommendations!
