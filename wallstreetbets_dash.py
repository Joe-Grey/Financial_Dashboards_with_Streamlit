import streamlit as st
import os
from dotenv import load_dotenv
import praw
from praw.models import MoreComments
import pandas as pd

def load_wallstreetbets_dash():
    reddit=praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
               client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
               uredirect_uri="http://localhost:8501",
               user_agent="testscript by u/fakebot3",)
    subreddit = reddit.subreddit('wallstreetbets')

    tickerlist=['GME', 'AMC', 'SPCE', 'FUBO', 'BBBY', 'LGND', 'FIZZ', 'SPWR', 'SKT', 'GSX', 'TR', 'GOGO', 'AXDX', 'BYND', 'OTRK', 'CLVS', 'RKT', 'SRG', 'IRBT', 'PRTS', 'PGEN', 'TSLA']

    num_limit = st.sidebar.slider("Limit on topics", min_value=1, max_value=200, value=10)

    hot = subreddit.hot(limit=num_limit)
    sum=[0]*len(tickerlist) # our output array
    counttotal=0 # total number of comment read
    submissions_counter=0

    for submissions in hot:
        if not submissions.stickied:
            submissions_counter+=1
            if submissions_counter>5:
                comments = submissions.comments
                for comment in comments:
                    if isinstance(comment, MoreComments):
                        continue
                    counttotal+=1
                    for i, ticker in enumerate(tickerlist):
                        if ticker in comment.body:
                            sum[i]=sum[i]+1
    

    output=pd.DataFrame(data={'Tick': tickerlist, 'Counts': sum})
    st.write('Total comments read: ',counttotal)
    st.write(output[output['Counts']>0])
