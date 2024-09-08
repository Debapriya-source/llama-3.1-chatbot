import os
import json

import streamlit as st
from groq import Groq


def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


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
    st.session_state.chat_history = [
        {"role": "assistant",
         "content":
         """
                    I'm your DSA buddy, here to help you ace those tech interviews and conquer coding challenges! 
                    Let's get started! What specific area would you like to explore today? 
                    Do you want to: 
                    - Discuss a particular problem or algorithm? 
                    - Practice with code examples?
                    - Review common interview questions?
                    - Optimize your coding workflow?
                    Type away, and let's dive into the world of DSA together!
                    """
         },
    ]

# page title
st.title("Welcome Buddy🤓!")
st.caption("Helping You Level Up Your Coding Game")
# the messages in chat_history will be stored as {"role":"user/assistant", "content":"msg}
# display chat history
for message in st.session_state.chat_history:
    # print("message in chat session")
    with st.chat_message("role", avatar='🤖'):
        st.markdown(message["content"])


# user input field
user_prompt = st.chat_input("Ask me")

if user_prompt:
    # st.chat_message("user").markdown
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    # get a response from the LLM
    messages = [
        {"role": "system", "content": """
            You are a world-leading expert on DSA.
            This includes but is not limited to: all the leetcode problems.
            You can prepare anyone for tech interviews in top tech companies.
            And wrap numbers in proper markdown formatting (ex: `123`).
            Provide the answers in a easier way.
            Prefer dry-run with example while explaining any concept.
            Always identify the common mistakes and how that could be resolved while providing sollution hints.
            Try be a cheerfull, excited and motivated assistant.
            Only answer the question - do not return something dumb like "[YourNextQuestion]"
         """
         },
        {"role": "assistant", "content": "Hey there! I can explain everything in DSA to a five year old, Lets help you out!"},
        *st.session_state.chat_history
    ]

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar='🤖'):
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            stream=True  # for streaming the message
        )
        response = st.write_stream(parse_groq_stream(stream))
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})
