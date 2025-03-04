import streamlit as st
import pandas as pd
import numpy as np
import os

# Set page title
st.title('My First Streamlit App')

# Add a header
st.header('Welcome to the Demo!')

# Add some text
st.write('This is a simple demonstration of Streamlit features.')

# Create a sidebar
st.sidebar.header('Sidebar Controls')

# Add a slider to the sidebar
number = st.sidebar.slider('Select a number:', 0, 100, 50)
st.write(f'You selected: {number}')

# Add a selectbox
option = st.selectbox(
    'What is your favorite color?',
    ['Red', 'Green', 'Blue', 'Yellow']
)
st.write(f'Your favorite color is {option}')

# Create some sample data
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

# Display a line chart
st.subheader('Line Chart Example')
st.line_chart(chart_data)

# Add a checkbox
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(chart_data) 