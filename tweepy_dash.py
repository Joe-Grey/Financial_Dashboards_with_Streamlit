import streamlit as st
import os
from dotenv import load_dotenv
import tweepy
import csv

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv("TWITTER_CONSUMER_API_KEY"), os.getenv("TWITTER_CONSUMER_API_KEY_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))

api = tweepy.API(auth)

def load_tweepy_dash():
    TWITTER_USERNAMES = list()
    TWITTER_USERNAMES.append('all')
    # List of popular traders usernames that we want to pull tweets from
    with open('twitter_usernames.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            TWITTER_USERNAMES.append(str(row).replace("['", "").replace("']", ""))
    
    user_select = st.sidebar.selectbox('Which Twitter user...?', TWITTER_USERNAMES, 1)

    if user_select == 'all':
        for username in TWITTER_USERNAMES:
            if username != 'all':
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
                

    else:
        user = api.get_user(user_select)
        tweets = api.user_timeline(user_select)

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