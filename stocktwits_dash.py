import streamlit as st
import requests

def load_socktwits_dash():
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