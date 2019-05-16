from __future__ import absolute_import, print_function
from tweepy import OAuthHandler, Stream, StreamListener
import time
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import sqlite3

# API keys
consumer_key = "#######"
consumer_secret = '######'
access_token = '########'
access_token_secret = "######"

# define connection
conn = sqlite3.connect('twitter.DB')
c = conn.cursor()
# instantiate Vader
analyzer = SentimentIntensityAnalyzer()


'''Create the table with the fields:
    unix(integer) - for the timestamp
    tweet(string) - the contents of the tweet
    sentiment(float) - sentiment score for the tweet
    lat(string) - latitude
    long(string) - longitude
    lang(string) - languange
'''


def create_table():
    try:
        c.execute(
            "CREATE TABLE IF NOT EXISTS got_sentiment(unix REAL, tweet TEXT, sentiment REAL, lat TEXT, long TEXT, lang TEXT)")
        c.execute("CREATE INDEX id_unix ON got_sentiment(unix)")
        c.execute("CREATE INDEX id_tweet ON got_sentiment(tweet)")
        c.execute("CREATE INDEX id_sentiment ON got_sentiment(sentiment)")
        c.execute("CREATE INDEX id_lat ON got_sentiment(lat)")
        c.execute("CREATE INDEX id_long ON got_sentiment(long)")
        c.execute("CREATE INDEX id_lang ON got_sentiment(lang)")
        conn.commit()
    except Exception as e:
        print(str(e))


# instantiate table
create_table()


class Listener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    It is also used to filter out data that we won't be capturing in the DB.
    Additionally, we will save the filtered data to the DB, in this case we want
    to only capture tweets in english (vader isn't multilingual), and if possible
    capture location of the tweet.
    """

    def on_data(self, data):
        # filters for only the necessary things to be saved in the db
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            vs = analyzer.polarity_scores(tweet)  # Run analysis on the tweet
            sentiment = vs['compound']
            lat = ''
            long = ''
            lang = ''
            if data['user']['lang'] and data['user']['lang'] == 'en':
                lang = data['user']['lang']
            if data['coordinates'] or data['geo']:
                lat = str(data['coordinates']['coordinates'][1])
                long = str(data['coordinates']['coordinates'][0])
            print(time_ms, tweet, sentiment, lat, long, lang)
            c.execute("INSERT INTO got_sentiment (unix, tweet, sentiment, lat, long, lang) VALUES (?, ?, ?, ?, ?, ?)",
                      (time_ms, tweet, sentiment, lat, long, lang))
            conn.commit()
            return True
        except KeyError as e:
            print(str(e))
        return True

    def on_error(self, status):
        print(status)


''' Main statement used to run the scrapper, if rate limit is hit, will sleep
for 5 seconds then reconnect
'''
while True:
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, Listener())
        stream.filter(track=['#gameofthrones'])
    except Exception as e:
        print(str(e))
        time.sleep(5)
