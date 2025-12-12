import streamlit as st
from backend import workflow
from langchain_core.messages import HumanMessage


config = {'configurable': {'thread_id': 'thread_1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Display existing chat messages
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# Chat input box
user_input = st.chat_input("Type here")

if user_input:
    # Store user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # Stream the assistant's response
    # with st.chat_message('assistant'):
    #     message_placeholder = st.empty()
    #     full_response = ""

    #     for message_chunk, metadata in workflow.stream(
    #         {'message': [HumanMessage(content=user_input)]},
    #         config=config,
    #         stream_mode='messages'    # <-- FIXED HERE (plural)
    #     ):
    #         content = getattr(message_chunk, "content", "")
    #         full_response += content
    #         message_placeholder.markdown(full_response)
    
    
    with st.chat_message('assistant'):
        
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in workflow.stream(
                {'message':[HumanMessage(content=user_input)]},
                config = {'configurable':{'thread_id':'thread_1'}},
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
