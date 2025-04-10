import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI

chatModel35 = ChatOpenAI(model="gpt-3.5-turbo-0125")
chatModel4o = ChatOpenAI(model="gpt-4o")

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

chatModel4o_with_tools = chatModel4o.bind_tools([multiply])

from langgraph.graph import MessagesState

class MessagesState(MessagesState):
    # Add any keys needed beyond messages, which is pre-built 
    pass

from langgraph.graph import MessagesState

# Node
def llm_with_tool(state: MessagesState):
    return {"messages": [chatModel4o_with_tools.invoke(state["messages"])]}

from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("llm_with_tool", llm_with_tool)
builder.add_node("tools", ToolNode([multiply]))

# Add the logic of the graph
builder.add_edge(START, "llm_with_tool")

builder.add_conditional_edges(
    "llm_with_tool",
    # If the input is a tool call -> tools_condition routes to tools
    # If the input is a not a tool call -> tools_condition routes to END
    tools_condition,
)

builder.add_edge("tools", END)

# Compile the graph
graph = builder.compile()


from pprint import pprint
from langchain_core.messages import HumanMessage

messages = [HumanMessage(content="What was the relationship between Lem Billings and JFK?")]

messages = graph.invoke({"messages": messages})

for m in messages['messages']:
    m.pretty_print()
    
messages = [HumanMessage(content="Multiply 4 and 5")]

messages = graph.invoke({"messages": messages})

for m in messages['messages']:
    m.pretty_print()
    
