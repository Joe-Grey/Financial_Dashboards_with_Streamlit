import streamlit as st
import pandas as pd
import numpy as np

st.title('This is the title')

st.header('This is a header')

st.subheader('This is a subheader')

st.write('This is regular text')

'''
# YOU CAN USE MARKDOWN
### Really cool
'''

st.subheader('You can define dictionaries & lists too:')
some_dict = {
    'key': 'value',
    'key2': 'value2'
}
some_list = [1,2,3]
st.write(some_dict)
st.write(some_list)


# Adding a sidebar
st.sidebar.write('Write this to the sidebar')

# Displaying a dataframe
st.subheader('Displaying a dataframe:')
df = pd.DataFrame(np.random.randn(50, 20),columns=('col %d' % i for i in range(20)))

st.dataframe(df)  # Same as st.write(df)
