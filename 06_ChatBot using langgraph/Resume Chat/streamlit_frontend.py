import streamlit as st
from langgraph_backend import workflow
from langchain_core.messages import HumanMessage
import uuid #with the help of this you can generate random thread_id each time



# utility funcation
def generate_thread_id():
    thread_id = uuid.uuid4()
    return str(thread_id)

 
 
def reset_chat():
    thread_id = generate_thread_id()
    add_thread(st.session_state['thread_id'])
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)
        


def load_conversation(thread_id):
    return workflow.get_state(config={'configurable':{'thread_id':thread_id}}).values['message']


  
        
# session setup

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()


if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread'] = []


add_thread(st.session_state['thread_id'])



# slide bar
st.sidebar.title('langgraph chatbot')


if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('conversation')


for thread_id in st.session_state['chat_thread'][::]:
     if  st.sidebar.button(thread_id):
        st.session_state['thread_id'] = thread_id
        message = load_conversation(thread_id)
         
         
        temp_message_dict = []
         
        for msg in message:
             if isinstance(message, HumanMessage):
                 role = 'user'
                 
             else:
                 role = 'assistant'
             temp_message_dict.append({'role':role, 'content':msg.content})
             
        st.session_state['message_history'] = temp_message_dict



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
 


    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
   
    
    with st.chat_message('assistant'):
        
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in workflow.stream(
                {'message':[HumanMessage(content=user_input)]},
                config = CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
