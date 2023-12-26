import tweepy

from openai import OpenAI

import os
from dotenv import load_dotenv

# Load .env variables.
load_dotenv()

# Create Tweepy API object.
tweepy_api = tweepy.Client(
    bearer_token=os.environ.get("TWITTER_BEARER_TOKEN"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
    consumer_key=os.environ.get("TWITTER_CONSUMER_KEY"),
    consumer_secret=os.environ.get("TWITTER_CONSUMER_SECRET")
)

# Create a tweet
# tweepy_api.create_tweet(text="Hello, world!")

# Initialize OpenAI.
openai_api = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Function to convert strings to booleans.

  

# Function to flip tweets.
def flip_tweet(tweet):
    chat_completion = openai_api.chat.completions.create(
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
    response = openai_api.moderations.create(
        input=tweet
    )
    
    for moderation in response.results:
        categories = moderation.categories
        # Check if any category other than harassment is true
        if (categories.harassment_threatening or categories.hate or 
            categories.hate_threatening or categories.self_harm or 
            categories.self_harm_instructions or categories.self_harm_intent or 
            categories.sexual or categories.sexual_minors or 
            categories.violence or categories.violence_graphic):
            return True
    return False

flipped_tweet = flip_tweet("")
print(flipped_tweet)
print(check_tweet(""))