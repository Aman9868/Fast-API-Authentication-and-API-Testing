import tweepy

def create_twitter_client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth.set_bearer_token(bearer_token)
    return tweepy.API(auth)

def get_user_followers(api):
    followers = api.followers_ids()
    return followers
