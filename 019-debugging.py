import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# This will be a tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, multiply, divide]
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

from IPython.display import Image, display

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# System message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

# Node
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine the control flow
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")

memory = MemorySaver()

graph = builder.compile(checkpointer=MemorySaver())

# Show
display(Image(graph.get_graph(xray=True).draw_mermaid_png()))

# Input
initial_input = {"messages": HumanMessage(content="Multiply 2 and 3")}

# Thread
thread = {"configurable": {"thread_id": "1"}}

# Run the graph until the first interruption
for event in graph.stream(initial_input, thread, stream_mode="values"):
    event['messages'][-1].pretty_print()
    
graph.get_state({'configurable': {'thread_id': '1'}})

all_states = [s for s in graph.get_state_history(thread)]

len(all_states)

all_states[-2]

step_to_replay = all_states[-2]

step_to_replay.config

step_to_replay.next

for event in graph.stream(None, step_to_replay.config, stream_mode="values"):
    event['messages'][-1].pretty_print()
    
step_to_fork = all_states[-2]
step_to_fork.values["messages"]

step_to_fork.config

# PAY ATTENTION: see how we enter the different input for the forked step
# Now the new input for the same step will be "Multiply 5 and 100"
# Instead of the previous input "Multiply 2 and 3"
fork_config = graph.update_state(
    step_to_fork.config,
    {"messages": [HumanMessage(content='Multiply 5 and 100', 
                               id=step_to_fork.values["messages"][0].id)]},
)

fork_config

all_states = [state for state in graph.get_state_history(thread) ]
all_states[0].values["messages"]

graph.get_state({'configurable': {'thread_id': '1'}})

for event in graph.stream(None, fork_config, stream_mode="values"):
    event['messages'][-1].pretty_print()
    
graph.get_state({'configurable': {'thread_id': '1'}})

