import tweepy
import openai
import os
import time
import schedule
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials from environment variables
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Thought leader's Twitter handle
thought_leader_handle = "berkson0"

# OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Authenticate with Twitter using OAuth1UserHandler
try:
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    tweepy_api = tweepy.API(auth)
except tweepy.TweepyException as e:
    print(f"Error: Twitter API authentication failed - {e}")
    exit(1)

def get_user_id(username):
    try:
        user = tweepy_api.get_user(screen_name=username)
        return user.id
    except tweepy.TweepyException as e:
        print(f"Error: Unable to fetch user ID - {e}")
        exit(1)

def reverse_thoughts(tweet):
    # Use OpenAI API to reverse the thoughts in the tweet
    prompt = f"Reverse the following tweet to express the opposite sentiment:\n\n{tweet}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60
    )
    reversed_tweet = response.choices[0].text.strip()
    return reversed_tweet

def get_latest_tweets(user_id):
    print("Fetching tweets is only available with paid API access.")
    return []

def post_tweet(status):
    try:
        # Use tweepy.API to post a new tweet
        tweepy_api.update_status(status)
    except tweepy.TweepyException as e:
        print(f"Error: Unable to post tweet - {e}")

def process_tweets(user_id):
    tweets = get_latest_tweets(user_id)
    for tweet in tweets:
        original_tweet = tweet.text
        reversed_tweet = reverse_thoughts(original_tweet)
        post_tweet(reversed_tweet)

def main():
    user_id = get_user_id(thought_leader_handle)
    schedule.every().day.at("10:00").do(process_tweets, user_id)  # Schedule the task to run once a day at 10:00 AM

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
