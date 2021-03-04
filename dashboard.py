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
dash_select = st.sidebar.selectbox('Which Dashboard?', ('twitter', 'wallstreetbets', 'stocktwits', 'chart', 'reddit', 'stock portfolio', 'stock prediction'), 5)

st.markdown(f"<h1 style='text-align: center;'>{dash_select.upper()}</h1>", unsafe_allow_html=True)

if dash_select == 'twitter':
    st.markdown(f"<h2 style='text-align: center;'>Getting tweets from known stock traders</h2>", unsafe_allow_html=True)
    tweepy_dash.load_tweepy_dash()

if dash_select == 'wallstreetbets':
    st.markdown(f"<h2 style='text-align: center;'>Getting a count of the number of times a particular stock is mentioned on the subreddit of wallstreetbets</h2>", unsafe_allow_html=True)
    wallstreetbets_dash.load_wallstreetbets_dash()

if dash_select == 'stocktwits':
    st.markdown(f"<h4 style='text-align: center;'>(Stocktwits is like Twitter for traders & investors)</h4>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Pulls the feed that mentions a particular stock</h2>", unsafe_allow_html=True)
    stocktwits_dash.load_socktwits_dash()

if dash_select == 'chart':
    st.markdown(f"<h2 style='text-align: center;'>Displays a particular stocks history on a chart and as a table</h2>", unsafe_allow_html=True)
    chart_dash.load_chart_dash()

if dash_select == 'reddit':
    st.markdown(f"<h2 style='text-align: center;'>Gets all the posts that mention stocks on the subreddit of wallstreetbets</h2>", unsafe_allow_html=True)
    reddit_dash.load_reddit_dash()

if dash_select == 'stock portfolio':
    st.markdown(f"<h2 style='text-align: center;'>From a selection of random stocks - this portfolio is what is reccomended you purcahse</h2>", unsafe_allow_html=True)
    # MAX 400 Tickers at this moment in time
    RANDOM_NUMBER_SELECTED = int(st.slider("Number of random stocks to select from....", min_value=1, max_value=300, value=50)) # The number used to select the number of element from a larger list 
    PORTFOLIO_VALUE = st.number_input('How much do you wnat to invest $$$....', value=1000) # The amount in $ you wish to invest
    if st.button('Click to start processing'):
        stock_portfolio_dash.load_portfolio_dash(RANDOM_NUMBER_SELECTED, PORTFOLIO_VALUE)

if dash_select == 'stock prediction':
    stock_prediction_dash.load_chart_dash()



    
    
