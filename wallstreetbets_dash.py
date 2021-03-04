import streamlit as st
import os
from dotenv import load_dotenv
import praw
from praw.models import MoreComments
import pandas as pd
import csv
import requests

# Create a function to get the companies name
def get_company_name(symbol):
    url = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query='+symbol+'&region=1&lang=en'
    result = requests.get(url).json()
    for r in result['ResultSet']['Result']:
        if r['symbol']==symbol:
            return r['name']

def load_wallstreetbets_dash():
    reddit=praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
               client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
               uredirect_uri="http://localhost:8501",
               user_agent="testscript by u/fakebot3",)
    subreddit = reddit.subreddit('wallstreetbets')

    # List of stock tickers
    tickerlist = list()
    with open('stock_ticker_list.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            tick_symbol = str(row).replace("['", "").replace("']", "")
            tickerlist.append(tick_symbol)

    st.sidebar.write()
    num_limit = st.sidebar.slider("Limit on topics (The bigger the number the longer it will take to load)", min_value=1, max_value=200, value=10)

    hot = subreddit.hot(limit=num_limit)
    sum=[0]*len(tickerlist) # our output array
    counttotal=0 # total number of comment read
    submissions_counter=0

    # So the pseudocode of what we want to do looks like this
    '''
    We are now ready to “read” comments.
    We will loop over the hot post.
    Check if the post (submission) is sticky?
    If it is sticky and we skipped the first few (5) posts.
    Get comments for the submission.
    If we get a “MoreComments” just skip for the next comment.
    Go over all tickers and see if a ticker is mentioned in the comment.
    '''

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
    
    
    

    output=pd.DataFrame(data={'Tick': tickerlist, 'Counts': sum}).sort_values(by=['Counts'], ascending=False)
    output = output[output['Counts'] > 50]  

    
    company_name = list()
    for row in output.iterrows():
        company_name.append(get_company_name(row[1][0]))
    
    output['Company'] = company_name
    st.write('Total comments read: ',counttotal)
    st.text('(Only displaying counts > 50)')
    st.write(output[output['Counts']>0])

