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

def fetch_tweets(username):
    user_id = tweepy_api.get_user(username=username).data.id
    responses = tweepy.Paginator(tweepy_api.get_users_tweets, user_id, max_results=100, limit=100)
    tweets_list = [["link", "username" "tweet"]]
    
    counter = 0
    for response in responses:
        counter += 1
        print(f"==> processing {counter * 100} to {(counter + 1) * 100} of {username}'s tweets")
        try:
            for tweet in response.data:  # see any individual tweet by id at: twitter.com/anyuser/status/TWEET_ID_HERE
                tweets_list.append([f"https://twitter.com/anyuser/status/{tweet.id}", username, tweet.text])
        except Exception as e:
            print(e)

    print("Done!")


flipped_tweet = flip_tweet("")
print(flipped_tweet)
print(check_tweet(""))