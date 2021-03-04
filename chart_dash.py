import streamlit as st
import yfinance as yf
import datetime as dt
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
import requests

# Create a function to get the companies name
def get_company_name(symbol):
    url = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query='+symbol+'&region=1&lang=en'
    result = requests.get(url).json()
    for r in result['ResultSet']['Result']:
        if r['symbol']==symbol:
            return r['name']

def load_chart_dash():

    YESTERDAY_DATE = dt.date.today() - dt.timedelta(days=1)
    stock_ticker = st.sidebar.text_input("Symbol", value='AAPL', max_chars=None, key=None, type='default').upper()
    start_date = st.sidebar.date_input("Select Start Date...", max_value=YESTERDAY_DATE, value=YESTERDAY_DATE + relativedelta(months=-1))
    try:
        # Get the data for the stock AAPL
        data = yf.download(stock_ticker,start_date,YESTERDAY_DATE).reset_index()

        st.markdown(f"<h1 style='text-align: center;'>{stock_ticker.upper} - {get_company_name(stock_ticker)}</h1>", unsafe_allow_html=True)

        fig = go.Figure(data=[go.Candlestick(x=data['Date'].dt.date,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'],
                        name=stock_ticker)])

        fig.update_xaxes(type='category')
        fig.update_layout(height=700)

        st.plotly_chart(fig, use_container_width=True)

        st.write(data)
    except:
        st.write("Cannot load data for: " + str(stock_ticker))