import streamlit as st
import requests

# Create a function to get the companies name
def get_company_name(symbol):
    url = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query='+symbol+'&region=1&lang=en'
    result = requests.get(url).json()
    for r in result['ResultSet']['Result']:
        if r['symbol']==symbol:
            return r['name']

def load_socktwits_dash():
    symbol_input = st.sidebar.text_input('Symbol input...', value='AAPL', max_chars=5, key=None, type='default').upper()
    try:
        req = requests.get(f'https://api.stocktwits.com/api/2/streams/symbol/{symbol_input}.json')
        data = req.json()
        st.markdown(f"<h1 style='text-align: center;'>{symbol_input.upper()} - {get_company_name(symbol_input)}</h1>", unsafe_allow_html=True)
        st.markdown('<hr>', unsafe_allow_html=True)
        for message in data['messages']:
            st.image(message['user']['avatar_url'])
            st.write(message['user']['username'])
            st.write(message['created_at'])
            st.write(message['body'])
            st.markdown('<hr>', unsafe_allow_html=True)
    except:
        st.write('Cannot get data for symbol entered - does the symbol exist?')