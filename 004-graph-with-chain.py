import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI

chatModel35 = ChatOpenAI(model="gpt-3.5-turbo-0125")
chatModel4o = ChatOpenAI(model="gpt-4o")

from langgraph.graph import MessagesState

class MessagesState(MessagesState):
    # Add any keys needed beyond messages, which is pre-built 
    pass

# Node
def simple_llm(state: MessagesState):
    return {"messages": [chatModel4o.invoke(state["messages"])]}

from langgraph.graph import StateGraph, START, END
    
# Build graph
builder = StateGraph(MessagesState)
builder.add_node("simple_llm", simple_llm)

# Add the logic of the graph
builder.add_edge(START, "simple_llm")
builder.add_edge("simple_llm", END)

# Compile the graph
graph = builder.compile()

from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage

messages = graph.invoke({"messages": HumanMessage(content="Where is the Golden Gate Bridge?")})

for m in messages['messages']:
    m.pretty_print()

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

chatModel4o_with_tools = chatModel4o.bind_tools([multiply])

# Node
def llm_with_tool(state: MessagesState):
    return {"messages": [chatModel4o_with_tools.invoke(state["messages"])]}

from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
    
# Build graph
builder = StateGraph(MessagesState)

builder.add_node("llm_with_tool", llm_with_tool)

# Add the logic of the graph
builder.add_edge(START, "llm_with_tool")
builder.add_edge("llm_with_tool", END)

# Compile the graph
graph = builder.compile()

from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage

# The following two lines are the most frequent way to 
# run and print a LangGraph chatbot-like app results.
messages = graph.invoke({"messages": HumanMessage(content="Where is the Eiffel Tower?")})

for m in messages['messages']:
    m.pretty_print()
    
from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage

# The following two lines are the most frequent way to 
# run and print a LangGraph chatbot-like app results.
messages = graph.invoke({"messages": HumanMessage(content="Multiply 4 and 5")})

for m in messages['messages']:
    m.pretty_print()