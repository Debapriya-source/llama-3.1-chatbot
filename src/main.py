import os
import json

import streamlit as st
from groq import Groq


# streamlit page configuration
st.set_page_config(
    page_title="llama-3.1 Chatbot",
    page_icon="🦙",
    layout="centered",
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

# save the api_key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# initialize the chat history if present as streamlit session
if "chat_history" not in st.session_state:
    # print("message not in chat session")
    st.session_state.chat_history = []

# page title
st.title("Welcome!")

# the messages in chat_history will be stored as {"role":"user/assistant", "content":"msg}
# display chat history
for message in st.session_state.chat_history:
    # print("message in chat session")
    with st.chat_message("role"):
        st.markdown(message["content"])


# user input field
user_prompt = st.chat_input("Ask me")

if user_prompt:
    # st.chat_message("user").markdown
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    # get a response from the LLM
    messages = [
        {"role": "assistant", "content": "You are a DSA teacher"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response})

    # display llm response
    with st.chat_message("assistant"):
        # st.markdown(assistant_response)
        st.markdown(assistant_response)
