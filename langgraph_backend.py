from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
load_dotenv()
llm=ChatGroq(model='meta-llama/llama-4-maverick-17b-128e-instruct')

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

connection=sqlite3.connect(database='chatbot_db',check_same_thread=False)
checkpointer=SqliteSaver(conn=connection)
graph=StateGraph(ChatState)

def chat_node(state:ChatState)->ChatState:
    messages=state['messages']
    response=llm.invoke(messages)
    return {'messages':messages+[response]}
    
    
#add node
graph.add_node('chat_node',chat_node)

# add edge
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

# compile
workflow=graph.compile(checkpointer=checkpointer)
# config = {'configurable': {'thread_id': 'thread_two'}}
# result=workflow.invoke(
#     {'messages':[HumanMessage('Which country did I asked?')]},
#     config=config
# )
# print(result)
def retrive_all():
    my_set=set()
    for checkpoint in checkpointer.list(None):
        my_set.add(checkpoint.config['configurable']['thread_id'])
    return list(my_set)

print(retrive_all())

# while True:
    
#     user_message=input("Enter your response")
#     print('Question: ',user_message)
#     if user_message.lower().strip() in ['bye','exit','quit']:
#         print('Good to have you here!')
#         break
#     config={'configurable':{'thread_id':thread_id}}
#     response=workflow.invoke({'messages':[HumanMessage(content=user_message)]},config=config)
#     print('AI response: ',response['messages'][-1].content)

# for message_chunk,metadata in workflow.stream(
#     {'messages':[HumanMessage(content='Tell me how to make pasta?')]},
#     stream_mode='messages',
#     config={'configurable':{'thread_id':thread_id}}
# ):
#     if message_chunk.content:
#         print(message_chunk.content,end='',flush=True)