import streamlit as st
import os
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set page configuration and title
st.set_page_config(page_title="Azure OpenAI Chat", layout="wide")
st.title('Azure OpenAI Chat Interface')

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# Get Azure OpenAI settings from environment variables
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Sidebar for settings
with st.sidebar:
    st.header('Chat Settings')
    
    # Display Azure OpenAI configuration (read-only)
    st.subheader("Azure OpenAI Configuration")
    st.text(f"Endpoint: {endpoint if endpoint else 'Not configured'}")
    st.text(f"Deployment: {deployment_name if deployment_name else 'Not configured'}")
    st.text(f"API Version: {api_version}")
    
    # Allow temperature adjustment
    st.subheader("Model Settings")
    temperature = st.slider('Temperature:', 0.0, 1.0, 0.7, step=0.1)
    
    if st.button('Clear Chat History'):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! How can I help you today?"}
        ]
        st.rerun()
    
    # Add some information
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This chat interface connects to Azure OpenAI using LangChain.")
    st.markdown("Configuration is loaded from the .env file.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Initialize Azure OpenAI client
def get_azure_openai_client():
    if not api_key or not endpoint or not deployment_name:
        st.error("Azure OpenAI settings are missing in the .env file. Please configure them.")
        return None
    
    try:
        client = AzureChatOpenAI(
            azure_deployment=deployment_name,
            openai_api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
            temperature=temperature
        )
        return client
    except Exception as e:
        st.error(f"Error initializing Azure OpenAI client: {str(e)}")
        return None

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response from Azure OpenAI
    client = get_azure_openai_client()
    
    with st.chat_message("assistant"):
        if client:
            # Convert chat history to LangChain message format
            langchain_messages = []
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_messages.append(AIMessage(content=msg["content"]))
                elif msg["role"] == "system":
                    langchain_messages.append(SystemMessage(content=msg["content"]))
            
            # Get response from Azure OpenAI
            with st.spinner("Thinking..."):
                try:
                    ai_response = client.invoke(langchain_messages)
                    response = ai_response.content
                except Exception as e:
                    response = f"Error: {str(e)}"
        else:
            response = "Please configure Azure OpenAI settings in the .env file to get AI responses."
        
        st.write(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})