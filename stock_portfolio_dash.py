# Importing libraries
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import time
import csv
import random
# Optimise the portfolio
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import streamlit as st

# Create a function to get the companies name
def get_company_name(symbol):
    url = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query='+symbol+'&region=1&lang=en'
    result = requests.get(url).json()
    for r in result['ResultSet']['Result']:
        if r['symbol']==symbol:
            return r['name']

def load_portfolio_dash(RANDOM_NUMBER_SELECTED_IN, PORTFOLIO_VALUE_IN):
    START_DATE_FOR_STOCK_PRICES = '2015-1-1' # When you want your Stocks to go back to
    STOCK_TICKERS_CSV = 'stock_ticker_list.csv'
    PERCENTAGE_TO_USE = 10 # The % in which the amount a column must have otherwise it will be deleted
    
    # MAX 400 Tickers at this moment in time
    RANDOM_NUMBER_SELECTED = RANDOM_NUMBER_SELECTED_IN # The number used to select the number of element from a larger list 
    PORTFOLIO_VALUE = PORTFOLIO_VALUE_IN # The amount in $ you wish to invest


    # Load the tickers list from the csv file of tickers names
    with open(STOCK_TICKERS_CSV, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    tickers_list_imported = []
    for d in data:
        ticker = str(d).replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        tickers_list_imported.append(ticker)

    # 2 tickers just to start the dataframe in the correct format
    tickers_list_start = ['AAPL', 'TSLA']

    # Fetching the data from the list of tickers
    data = yf.download(tickers_list_start,START_DATE_FOR_STOCK_PRICES)['Adj Close']
    df = pd.DataFrame(data)

    ticker_count = 0

    LIST_TO_USE = random.sample(tickers_list_imported, RANDOM_NUMBER_SELECTED)
    #LIST_TO_USE = tickers_list_imported

    progress_count = 0
    my_progress_bar = st.progress(progress_count)
    val_to_progress_up = (100/len(LIST_TO_USE))/100

    for i in range(len(LIST_TO_USE)):
        if ticker_count > 0 and ticker_count % 300 == 0:
            #df.to_csv ('stock_dataframe.csv', index=True, header=True)
            st.write('\nSleeping for 2 Minutes\n')
            time.sleep(120)    
        ticker_count = ticker_count + 1
        data_new_col_name = str(LIST_TO_USE[i])
        #st.write('\n' + str(ticker_count) + '/' + str(len(LIST_TO_USE)) + ' - Downloading: ' + data_new_col_name)
        try:
            data_new = yf.download(LIST_TO_USE[i],START_DATE_FOR_STOCK_PRICES)['Adj Close']
            df[data_new_col_name] = data_new
        except:
            continue
        progress_count = progress_count + val_to_progress_up
        if progress_count <= 1:
            my_progress_bar.progress(progress_count)
        else:
            my_progress_bar.progress(100)

    #Drooping stock values
    no_data_for_ticker_list = []
    row_count_based_on_percentage = int(len(df)*(PERCENTAGE_TO_USE/100))
    for (columnName, columnData) in df.iteritems():
        if df[columnName].isnull().all():
            #st.write('Dropping : ' + str(columnName) + ' - it is all NAN')
            no_data_for_ticker_list.append(df.columns.get_loc(columnName))
        #elif df[columnName].count() < row_count_based_on_percentage:
        #    st.write('Dropping : ' + str(columnName) + ' - < than ' + str(PERCENTAGE_TO_USE) + '% of then number of rows')
        #    no_data_for_ticker_list.append(df.columns.get_loc(columnName))

    df = df.drop(df.columns[no_data_for_ticker_list], axis=1)

    # Creating a csv file
    #df.to_csv ('stock_dataframe.csv', index=True, header=True)

    # Calculate the expected annualised returns and the annualised sample covariance matrix of the daily asset returns
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # Optimise for the maximal Sharpe ratio - describes how much excess return you recieve from the extra volitility you endure for holding a riskier asset 
    ef = EfficientFrontier(mu, S) # Create the Efficient Frontier object
    raw_weights = ef.max_sharpe() # maximise the Sharpe Ratio and get the raw weights

    # Helper method to clean the raw weights setting any weights whos absolute values are below the cut off point to zero and rounding the rest
    # can cause some rounding errors - should not be off by a lot just good to know
    cleaned_weights = ef.clean_weights()

    # Get the discret allocations of each share per stock and the leftover money from investment
    latest_price = get_latest_prices(df)
    weights = cleaned_weights
    da = DiscreteAllocation(weights, latest_price, total_portfolio_value = PORTFOLIO_VALUE)
    allocation, leftover = da.lp_portfolio()

    # Store the company name into a list & Get descrete allocation values
    company_name = []
    discrete_allocation_list = []
    for symbol in allocation:
        company_name.append(get_company_name(symbol))
        discrete_allocation_list.append(allocation.get(symbol))

    # Create the portfolio
    # Create DF for portfolio
    portfolio_df = pd.DataFrame(columns=['Company_Name', 'Company_Ticker', 'Discrete_val_'+str(PORTFOLIO_VALUE)])

    # Add data to portfolio df 
    portfolio_df['Company_Name'] = company_name
    portfolio_df['Company_Ticker'] = allocation
    portfolio_df['Discrete_val_'+str(PORTFOLIO_VALUE)] = discrete_allocation_list

    # How the portfolio would expect to return
    perf = ef.portfolio_performance(verbose=True)
    st.write()
    st.write('Any Sharpe ratio over 1.0 is considered acceptable to good buy investment:')
    st.write('Expected annual return:', round(perf[0],2),'%')
    st.write('Annual volatility:',round(perf[1],2),'%')
    st.write('Sharpe Ratio:', round(perf[0],2))
    st.write()
    st.write('Funds Remaining: $', round(leftover,2))

    # Show the portfolio
    st.write(portfolio_df)