import streamlit as st
from psaw import PushshiftAPI
import datetime as dt
import time

api = PushshiftAPI()

def load_reddit_dash():
    num_limit = st.sidebar.slider("Limit on topics...", min_value=0, max_value=1000, value=100)
    YESTERDAY_DATE = dt.date.today() - dt.timedelta(days=1)
    start_time = int(dt.datetime(YESTERDAY_DATE.year, YESTERDAY_DATE.month, YESTERDAY_DATE.day).timestamp())

    if num_limit > 0:
        submissions = list(api.search_submissions(after=start_time,
                                    subreddit='wallstreetbets',
                                    filter=['url', 'author', 'title', 'subreddit'],
                                    limit=num_limit))
    else:
        submissions = list(api.search_submissions(after=start_time,
                                    subreddit='wallstreetbets',
                                    filter=['url', 'author', 'title', 'subreddit']))

    for submission in submissions:

        words = submission.title.split()
        cashtags = list(set(filter(lambda word: word.lower().startswith('$') and word[1:].lower().isalpha(), words)))
        
        if len(cashtags) > 0:
            if len(cashtags) > 1:
                for tag in cashtags:
                    st.subheader(tag)
            else:
                st.subheader(cashtags[0])
            
            st.write(submission.created_utc)
            st.write(submission.title)
            st.write(submission.url)
            st.markdown('<hr>', unsafe_allow_html=True)
