import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI

chatModel35 = ChatOpenAI(model="gpt-3.5-turbo-0125")
chatModel4o = ChatOpenAI(model="gpt-4o")

from typing_extensions import TypedDict

class State(TypedDict):
    graph_state: str

def node_1(state):
    print("---Node 1---")
    return {"graph_state": state['graph_state'] +" I will vote for"}

def node_2(state):
    print("---Node 2---")
    return {"graph_state": state['graph_state'] +" Donald Trump."}

def node_3(state):
    print("---Node 3---")
    return {"graph_state": state['graph_state'] +" Kamala Harris."}

import random
from typing import Literal

def decide_vote(state) -> Literal["node_2", "node_3"]:
    """
    Decide on the next node to visit based on a 60/40 probability split.
    """
    # Simulating a 60% probability for "node_2"
    if random.random() < 0.6:  # 60% chance
        return "node_2"
    
    # Remaining 40% chance
    return "node_3"

from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Add the logic of the graph
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_vote)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Compile the graph
graph = builder.compile()

response = graph.invoke({"graph_state" : "Hi, this is Joe Biden."})


print("\n----------\n")

print(response["graph_state"])

print("\n----------\n")

