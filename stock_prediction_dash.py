import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import pandas_datareader as web
import numpy as np
import pandas as pd
import requests
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
plt.style.use('fivethirtyeight')
import streamlit as st

# Create a function to get the companies name
def get_company_name(symbol):
    url = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query='+symbol+'&region=1&lang=en'
    result = requests.get(url).json()
    for r in result['ResultSet']['Result']:
        if r['symbol']==symbol:
            return r['name']

def load_chart_dash():

    YESTERDAY_DATE = dt.date.today() - dt.timedelta(days=1)
    STOCK_TICKER = st.sidebar.text_input("Symbol", value='AAPL', max_chars=5, key=None, type='default')
    GET_STOCK_FROM_SELECTED_STOCK_START_DATE = st.sidebar.date_input("Select Start Date...", max_value=YESTERDAY_DATE, value=YESTERDAY_DATE + relativedelta(months=-12))
    DAYS_TO_FUTURE_PREDICT = int(st.sidebar.slider("Days ahread to predict...", min_value=1, max_value=365, value=30)) # Number of days for our model to predict in the future

    # Get the stock quote
    df = web.DataReader(STOCK_TICKER, data_source='yahoo', start=GET_STOCK_FROM_SELECTED_STOCK_START_DATE, end=YESTERDAY_DATE)
    df = df.iloc[::-1]

    st.subheader(f'Stock price history for: {get_company_name(STOCK_TICKER)}')
    st.write(df.iloc[::-1]) # Printing in reverse order so the latest date shows first

    # Get the Adjusted CLose price - INDEPENDANT VARIABLE
    df = df[['Adj Close']]

    # Create a new column (the target or DEPENDANT variable) shifted DAYS_TO_FUTURE_PREDICT units up
    df['Prediction'] = df[['Adj Close']].shift(-DAYS_TO_FUTURE_PREDICT)

    ### Create the independant dataset (X) ###
    # Convert the dataframe to an numpy array
    X = np.array(df.drop(['Prediction'], 1))

    # Remove the last 'DAYS_TO_FUTURE_PREDICT' rows (removing the NaNs after shift)
    X = X[:-DAYS_TO_FUTURE_PREDICT]

    
    ### Create the dependant dataset (Y) ###
    # Convert the dataframe to an numpy array (All the values including the NaNs)
    Y = np.array(df['Prediction'])

    # Get all of the Y values except the last 'DAYS_TO_FUTURE_PREDICT' rows
    Y = Y[:-DAYS_TO_FUTURE_PREDICT]

    ''' Note
    X is a list of lists / Y is a list
    '''

    # Split the data into 80% training and 20% testing
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    # Create and train the Support Vector Machine (Regressor)
    svm_svr = SVR(kernel='rbf', C=1e3, gamma=0.1) # Support Vector model created
    svm_svr.fit(x_train, y_train) # train the Support Vector model

    # Create and train the Linear Regression Model
    lr = LinearRegression()
    lr.fit(x_train, y_train)

    # Testing model
    st.header('TESTING THE MODELS:')
    st.write('(Score returns the coefficient of determination R^2 of the prediction - best possible score is 1.0)')
    svr_confidence = svm_svr.score(x_test, y_test)
    st.subheader('Testing Support Vector Model Score:')
    st.write('Score:', svr_confidence)

    lr_confidence = lr.score(x_test, y_test)
    st.subheader('Testing Linear Regression Model:')
    st.write('Score:', lr_confidence)

    if svr_confidence > lr_confidence:
        st.subheader('Support Vector scored better than Linear Regression')
    else:
        st.subheader('Linear Regression scored better than Support Vector')
    
    ### Set the values we want to forcast on ###
    # Set 'DAYS_TO_FUTURE_PREDICT' equal to the last DAYS_TO_FUTURE_PREDICT rows of the original dataset from Adj. Close cloumn
    df_predictions = np.array(df.drop(['Prediction'], 1))[-DAYS_TO_FUTURE_PREDICT:]

    # Making predictions
    svm_predictions = svm_svr.predict(df_predictions)
    lr_predictions = lr.predict(df_predictions)

    # Creating the list dates for the future predictions dataframe
    list_of_future_dates = list()
    for future_day in range(1, len(svm_predictions)+1):
        date = YESTERDAY_DATE + timedelta(days=future_day)
        list_of_future_dates.append(date.strftime('%b %d, %Y'))

    #Print the predictions for the next 'DAYS_TO_FUTURE_PREDICT' days
    #    Converting numpy array to dataframe to make it look nicer on screen
    st.subheader('Support Vector Predictions for the next ' + str(DAYS_TO_FUTURE_PREDICT) + ' days:')
    svm_predictions_df = pd.DataFrame(svm_predictions, columns = ['Adj Close'], index=list_of_future_dates)
    st.write(svm_predictions_df)

    st.subheader('\nLinear Regression Predictions for the next ' + str(DAYS_TO_FUTURE_PREDICT) + ' days:')
    lr_predictions_df = pd.DataFrame(lr_predictions, columns = ['Adj Close'], index=list_of_future_dates)
    st.write(lr_predictions_df)

    
    #get_SVM_best_prices():
    st.header('SVM prediction loop to find out when to buy & sell')
    set_buy_price = 1000000000 # 1 million
    set_buy_price_date = dt.datetime.now().date()
    set_sell_price = -1000000000 # -1 million
    set_sell_price_date = dt.datetime.now().date()

    first_date = YESTERDAY_DATE + timedelta(days=1)
    for future_day in range(1, len(svm_predictions)+1):
        future_price = svm_predictions[future_day-1]
        future_date = YESTERDAY_DATE + timedelta(days=future_day)
        if future_price < set_buy_price:
            set_buy_price = future_price
            set_buy_price_date = future_date
        elif future_price > set_sell_price:
            set_sell_price = future_price
            set_sell_price_date = future_date
        last_date = YESTERDAY_DATE + timedelta(days=future_day)

    st.text('Date started:' + str(first_date.strftime('%b %d, %Y')) +'\tDate ended:' + str(last_date.strftime('%b %d, %Y')))
    st.write('\nThe lowest & highest buy & sell prices within the next ' + str(DAYS_TO_FUTURE_PREDICT) + ' days:')
    st.text('\nLOWEST Buy Price:\t' + str(set_buy_price_date.strftime('%b %d, %Y')) + '\t$' + str(round(set_buy_price,2)))
    st.text('HIGHEST Sell PRICE:\t' + str(set_sell_price_date.strftime('%b %d, %Y')) + '\t$' + str(round(set_sell_price,2)))
    st.text('\nDifference: $' + str(round(set_sell_price - set_buy_price,2)))

    # get_LR_best_prices():
    st.header('\nLR prediction loop to find out when to buy & sell')
    set_buy_price = 1000000000 # 1 million
    set_buy_price_date = dt.datetime.now().date()
    set_sell_price = -1000000000 # -1 million
    set_sell_price_date = dt.datetime.now().date()

    first_date = YESTERDAY_DATE + timedelta(days=1)
    for future_day in range(1, len(lr_predictions)+1):
        future_price = lr_predictions[future_day-1]
        future_date = YESTERDAY_DATE + timedelta(days=future_day)
        if future_price < set_buy_price:
            set_buy_price = future_price
            set_buy_price_date = future_date
        elif future_price > set_sell_price:
            set_sell_price = future_price
            set_sell_price_date = future_date
        last_date = YESTERDAY_DATE + timedelta(days=future_day)

    st.text('Date started:' + str(first_date.strftime('%b %d, %Y')) +'\tDate ended:' + str(last_date.strftime('%b %d, %Y')))
    st.write('\nThe lowest & highest buy & sell prices within the next ' + str(DAYS_TO_FUTURE_PREDICT) + ' days:')
    st.text('\nLOWEST Buy Price:\t' + str(set_buy_price_date.strftime('%b %d, %Y')) + '\t$' + str(round(set_buy_price,2)))
    st.text('HIGHEST Sell PRICE:\t' + str(set_sell_price_date.strftime('%b %d, %Y')) + '\t$' + str(round(set_sell_price,2)))
    st.text('\nDifference: $' + str(round(set_sell_price - set_buy_price,2)))