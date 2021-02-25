import streamlit as st
import stocktwits_dash
import tweepy_dash
import wallstreetbets_dash

# Adding a sidebar
st.sidebar.title('Options')

    # Adding selectbox to sidebar
dash_select = st.sidebar.selectbox('Which Dashboard?', ('twitter', 'wallstreetbets', 'stocktwits', 'chart', 'pattern'), 1)

st.markdown(f"<h1 style='text-align: center;'>{dash_select}</h1>", unsafe_allow_html=True)

if dash_select == 'twitter':
    tweepy_dash.load_tweepy_dash()

if dash_select == 'wallstreetbets':
    wallstreetbets_dash.load_wallstreetbets_dash()

if dash_select == 'stocktwits':
    stocktwits_dash.load_socktwits_dash()

if dash_select == 'chart':
    st.subheader('this is the chart dashboard')

if dash_select == 'pattern':
    st.subheader('this is the pattern dashboard')
    
    
