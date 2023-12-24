import tweepy

from openai import OpenAI

import os
from dotenv import load_dotenv

# Load .env variables.
load_dotenv()

# Authenticate with Twitter.
auth = tweepy.OAuthHandler(os.environ.get("TWITTER_CONSUMER_KEY"), os.environ.get("TWITTER_CONSUMER_SECRET"))
auth.set_access_token(os.environ.get("TWITTER_ACCESS_TOKEN"), os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"))

# Create Tweepy API object
tweepy_api = tweepy.API(auth)

# Create a tweet
tweepy_api.update_status("Hello Tweepy")

# Initialize OpenAI.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Function to convert strings to booleans.
def str_to_bool(str):
  if str == "True":
    return True
  else:
     return False

# Function to flip tweets.
def flip_tweet(tweet):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a Twitter bot that tweets the opposite of what a Twitter thought leader influencer says and is therefore just as insightful.",
            },
            {
                "role": "user",
                "content": f'Tweet: {tweet}',
            }
        ],
        model="gpt-3.5-turbo-1106",
    )
    response = chat_completion.choices[0].message.content
    return response

# Function to make sure the bot doesn't accidentally say something horrible.
def check_tweet(tweet):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You make sure that a Twitter bot that tweets the opposite of what a Twitter thought leader influencer says and is therefore just as insightful doesn't say anything really bad, like bomb palestine or kill all jews. The point of the bot is to be funny and vaguely sarcastic. Response with True if its a really bad tweet, and False to go ahead and post. Make sure your response works as a Python bool, cause it's gonna get passed into code.",
            },
            {
                "role": "user",
                "content": f'Tweet: {tweet}',
            }
        ],
        model="gpt-3.5-turbo-1106",
    )
    response = chat_completion.choices[0].message.content
    return str_to_bool(response)

flipped_tweet = flip_tweet("")
print(flipped_tweet)
print(check_tweet("Kill all Americans. Those fat idiots need to die."))