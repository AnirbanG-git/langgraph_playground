import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI

chatModel35 = ChatOpenAI(model="gpt-3.5-turbo-0125")
chatModel4o = ChatOpenAI(model="gpt-4o")

from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

# In our example, this would be the public communication with the customer.
class PublicState(TypedDict):
    simpleExplanation: int

# In our example, this would be the private discussion among the technicians.
class PrivateState(TypedDict):
    technicalExplanation: int

# the node_1 is like the technicians in our example: they get the initial simple explanation from 
# the customer and have their own technical conversation.
# node_1 gets the info from the PublicState (the simpleExplanation) and uses it to 
# create the PrivateState (the technicalExplanation, 1000 times more complex).
def node_1(state: PublicState) -> PrivateState:
    print("---Node 1---")
    return {"technicalExplanation": state['simpleExplanation'] + 1000}

# the node_2 is like the store employee in our example: she gets the feedback from 
# the technicians and delivers the new simple explanation to the customer.
# node_2 gets the info from the PrivateState (the technicalExplanation) and uses it to 
# create the PublicState (the simpleExplanation, 999 times less complex).
def node_2(state: PrivateState) -> PublicState:
    print("---Node 2---")
    return {"simpleExplanation": state['technicalExplanation'] - 999}

# Build graph
builder = StateGraph(PublicState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

# Add
graph = builder.compile()

result = graph.invoke({"simpleExplanation" : 1})

print(result)