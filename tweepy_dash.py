import streamlit as st
import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv("TWITTER_CONSUMER_API_KEY"), os.getenv("TWITTER_CONSUMER_API_KEY_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))

api = tweepy.API(auth)


# List of popular traders usernames that we want to pull tweets from
TWITTER_USERNAMES = [
    'traderstewie',
    'the_chart_life',
    'canuck2usa',
    'sunrisetrader',
    'tmltrader'
]

def load_tweepy_dash():
    for username in TWITTER_USERNAMES:
        user = api.get_user(username)
        tweets = api.user_timeline(username)

        col1, mid, col2 = st.beta_columns([1,1,20])
        with col1:
            st.image(user.profile_image_url, width=60)
        with col2:
            usr_nme = str(user.name) + ' (' + str(user.screen_name) + ')'
            st.subheader(usr_nme)

        for tweet in tweets:
            if '$' in tweet.text: # if the tweet contains a stock
                words = tweet.text.split(' ') #Splitting text up into a list of words
                for word in words:
                    if word.startswith('$') and word[1:].isalpha(): #if the word starts with $ and the rest of the word is alpha numeric (not a price)
                        symbol = word[1:] # Getting the stock symbol from the tweet
                        st.write(symbol)
                        st.write(tweet.created_at)
                        st.write(tweet.text)
                        # Displaying finviz stock chart with symbol
                        st.image(f'https://finviz.com/chart.ashx?t={symbol}')
                        st.markdown('<hr>', unsafe_allow_html=True)