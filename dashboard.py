import streamlit as st
import pandas as pd
import numpy as np
import requests

# Adding a sidebar
st.sidebar.title('Options')

    # Adding selectbox to sidebar
dash_select = st.sidebar.selectbox('Which Dashboard?', ('twitter', 'wallstreetbets', 'stocktwits', 'chart', 'pattern'))

st.header(dash_select)

if dash_select == 'twitter':
    st.subheader('twitter dashboard logic')

if dash_select == 'chart':
    st.subheader('this is the chart dashboard')

if dash_select == 'stocktwits':
    symbol_imput = st.sidebar.text_input('Symbol input...', value='AAPL', max_chars=5, key=None, type='default')
    try:
        req = requests.get(f'https://api.stocktwits.com/api/2/streams/symbol/{symbol_imput}.json')
        data = req.json()
        st.markdown(f"<h1 style='text-align: center;'>{symbol_imput}</h1>", unsafe_allow_html=True)
        st.markdown('<hr>', unsafe_allow_html=True)
        for message in data['messages']:
            st.image(message['user']['avatar_url'])
            st.write(message['user']['username'])
            st.write(message['created_at'])
            st.write(message['body'])
            st.markdown('<hr>', unsafe_allow_html=True)
    except:
        st.write('Cannot get data for symbol entered - does the symbol exist?')
    
    
