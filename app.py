#pip install streamlit langchain langchain-openai beautifulsoup4 python-dotenv chromadb

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever

load_dotenv()

def get_response(user_input):
    return "Hey mate"

def get_vectorstore_from_url(url):
    #get the text in document format
    loader = WebBaseLoader(url) 
    documents = loader.load()
    
    #split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(documents)

    #create a vectorstore from the chunks
    vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())
    
    return vector_store

def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI

    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages ([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query in order to find relevant information"),

    ])

    retriever_chain = create_history_aware_retriever( llm, retriever, prompt)

    return retriever_chain

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
    vector_store = get_vectorstore_from_url(website_url)
   
    retriever_chain = get_context_retriever_chain(vector_store)

    # user input  
    user_query = st.chat_input("Welcome to AO chatbot")
    if user_query is not None and user_query != "": 

        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

        retrieved_documents = retriever_chain.invoke({
            "chat_history": st.session_state.chat_history,
            "input": user_query
        })
        st.write(retrieved_documents)



    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

    