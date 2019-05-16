# Game of Thrones sentiment analysis Dash app
Game of Thrones sentiment analysis Dash app.
This project was done to stream & capture twitter data for season 8 episode 5 of Game of Thrones.
NLP was utilized to interpret the text data of each tweet.
The code in its current state is set to run locally.

# The libraries utilized were:
- VaderSentiment- NLP 
- Dash - Interactive dashboard
- Pandas - Data cleaning and analysis 
- Tweepy - Easily utilize twitter API for streaming
- sqlite - Database to store tweets
- Mapbox - Interactive Map

# The Dash board has 2 main components:
- The sentiment over time chart has a drop down menu in order to select various characters/events for which you wish to
  view the results for.
- The map, is interactive and plots the locations of each tweets.

![dash_app](https://user-images.githubusercontent.com/22856033/57848990-d47d5600-779f-11e9-9c7f-a98826f849da.gif)

# Cloning Instructions
# Prerequesites:
- Have Python 3.6, PIP, and virtualenv installed.

# Getting Started:
- Clone the repo.
- Run 'pip install -r requirements.txt' in order to install dependencies.
- Put in mapbox API key into the 'got_sentiment_dash_app.py' file.
- Put in twitter API keys into the 'got_stream_scrapper.py' file.

# Data collection
- To build the database & collect the data needed for app run the file 'got_stream_scrapper.py' file.
- This will construct the table with the necessary fields and automatically connect to twitter's stream and parse 
  for any tweet with '#gameofthrones'.
- The tweets will then get parsed for other fields like language, longitude, and latitude as well.
- Additionally, Vader Sentiment is applied at this step of the stream, and the compound score is inserted into its
  own field. 
  
# Alternative to data collection
- Download the sqlite DB with data collected from the airing of the episode to about 3 hours later via this link:     https://www.dropbox.com/s/zyzyrd4xpt0pdn0/twitter.DB?dl=1

# Running the server
- Before this step can happen, the previous steps must occur, since it will require a connection to the DB, an error
  will occur if a DB does not exist. 
- In the command line run 'python got_sentiment_dash_app.py'.
- It should start the server and run the app on 'localhost' port:8050.
- Copy this link to your browser.
