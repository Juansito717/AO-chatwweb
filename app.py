import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

def get_response(user_input):
    return "Hey mate"


# app config
st.set_page_config(page_title="AO chatbot")
st.title ("AOOO")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content= "Hey, lets start your journey"),
    ]

# sidebar
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")

if website_url is None or website_url == "":
    st.info("Nope, sorry") 

else:
    # user input  
    user_query = st.chat_input("Welcome to AO chatbot")
    if user_query is not None and user_query != "": 

        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

    