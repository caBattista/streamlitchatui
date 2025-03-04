import streamlit as st

# Set page title
st.title('My First Streamlit App')
#*
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

if __name__ == '__main__':     
    st.set_option('server.enableCORS', True)