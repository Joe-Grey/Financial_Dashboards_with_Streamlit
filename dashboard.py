import streamlit as st
import stocktwits_dash
import tweepy_dash
import wallstreetbets_dash
import chart_dash
import reddit_dash
import stock_prediction_dash

# Adding a sidebar
st.sidebar.title('Options')

    # Adding selectbox to sidebar
dash_select = st.sidebar.selectbox('Which Dashboard?', ('twitter', 'wallstreetbets', 'stocktwits', 'chart', 'test_reddit', 'stock prediction'), 5)

st.markdown(f"<h1 style='text-align: center;'>{dash_select}</h1>", unsafe_allow_html=True)

if dash_select == 'twitter':
    tweepy_dash.load_tweepy_dash()

if dash_select == 'wallstreetbets':
    wallstreetbets_dash.load_wallstreetbets_dash()

if dash_select == 'stocktwits':
    stocktwits_dash.load_socktwits_dash()

if dash_select == 'chart':
    chart_dash.load_chart_dash()

if dash_select == 'test_reddit':
    reddit_dash.load_reddit_dash()

if dash_select == 'stock prediction':
    stock_prediction_dash.load_chart_dash()
    
    
