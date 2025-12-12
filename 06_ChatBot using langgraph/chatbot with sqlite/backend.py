from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3


load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class ChatState(TypedDict):
    message: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    message = state["message"]
    for chunk in model.stream(message):
        yield {"message": [chunk]}   # Streaming generator



conn = sqlite3.connect(database='chatbot.db', check_same_thread=False) 
checkpointer = SqliteSaver(conn = conn)



graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


workflow = graph.compile(checkpointer=checkpointer)



def retrieve_all_thread():
    all_thread = set()
    for checkpoint in checkpointer.list(None):
        all_thread.add(checkpoint.config['configurable']['thread_id'])
        
    return list(all_thread)