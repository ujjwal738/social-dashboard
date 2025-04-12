import tweepy
from django.conf import settings

def get_twitter_client():
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    return tweepy.API(auth)

def fetch_tweets(username):
    client = get_twitter_client()
    tweets = client.user_timeline(screen_name=username, count=5, tweet_mode='extended')
    return [{'text': tweet.full_text, 'created_at': tweet.created_at} for tweet in tweets]
