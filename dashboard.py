import streamlit as st
import stocktwits_dash

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
    stocktwits_dash.load_socktwits_dash()
    
    
