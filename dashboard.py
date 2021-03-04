import streamlit as st
import stocktwits_dash
import tweepy_dash
import wallstreetbets_dash
import chart_dash
import reddit_dash
import stock_prediction_dash
import stock_portfolio_dash

# Adding a sidebar
st.sidebar.title('Options')

    # Adding selectbox to sidebar
dash_select = st.sidebar.selectbox('Which Dashboard?', ('twitter', 'wallstreetbets', 'stocktwits', 'chart', 'test_reddit', 'stock prediction', 'stock portfolio'), 1)

st.markdown(f"<h1 style='text-align: center;'>{dash_select}</h1>", unsafe_allow_html=True)

if dash_select == 'twitter':
    st.markdown(f"<h2 style='text-align: center;'>Getting tweets from known stock traders</h2>", unsafe_allow_html=True)
    tweepy_dash.load_tweepy_dash()

if dash_select == 'wallstreetbets':
    st.markdown(f"<h2 style='text-align: center;'>Getting a count of the number of times a particular stock is mentioned</h2>", unsafe_allow_html=True)
    wallstreetbets_dash.load_wallstreetbets_dash()

if dash_select == 'stocktwits':
    stocktwits_dash.load_socktwits_dash()

if dash_select == 'chart':
    chart_dash.load_chart_dash()

if dash_select == 'test_reddit':
    reddit_dash.load_reddit_dash()

if dash_select == 'stock prediction':
    stock_prediction_dash.load_chart_dash()

if dash_select == 'stock portfolio':
    # MAX 400 Tickers at this moment in time
    RANDOM_NUMBER_SELECTED = int(st.slider("Number of random stocks to select from....", min_value=1, max_value=400, value=50)) # The number used to select the number of element from a larger list 
    PORTFOLIO_VALUE = st.number_input('How much do you wnat to invest $$$....', value=1000) # The amount in $ you wish to invest
    if st.button('Click to start processing'):
        stock_portfolio_dash.load_portfolio_dash(RANDOM_NUMBER_SELECTED, PORTFOLIO_VALUE)

    
    
