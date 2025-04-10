import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI

chatModel35 = ChatOpenAI(model="gpt-3.5-turbo-0125")
chatModel4o = ChatOpenAI(model="gpt-4o")

from langgraph.graph import MessagesState

class State(MessagesState):
    summary: str
    
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage

# Define the logic to call the LLM model
def call_model(state: State):
    
    # Get the summary if it exists
    summary = state.get("summary", "")

    # If there is a summary, add it to system message and append it to messages
    if summary:
        
        # Add the summary to the system message
        system_message = f"Summary of previous conversation: {summary}"

        # Append the summary of the conversation to the next messages
        messages = [SystemMessage(content=system_message)] + state["messages"]
    
    # If there is no summary, messages remain as they are
    else:
        messages = state["messages"]
    
    response = model.invoke(messages)
    
    return {"messages": response}

def summarize_conversation(state: State):
    
    # First, we get the existing summary
    summary = state.get("summary", "")

    # Prompt if summary already exists 
    if summary:
        
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )

    # Prompt if summary does not exist yet
    else:
        summary_message = "Create a summary of the conversation above:"

    # Add summary to messages
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    
    response = model.invoke(messages)
    
    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    
    return {"summary": response.content, "messages": delete_messages}

from langgraph.graph import END

# Determine whether to end or summarize the conversation
def should_continue(state: State):
    
    """Return the next node to execute."""
    
    messages = state["messages"]
    
    # If there are more than six messages, 
    # then we will summarize the conversation
    if len(messages) > 6:
        return "summarize_conversation"
    
    # Otherwise we can just end
    return END

from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START

# Define a new graph
workflow = StateGraph(State)

# PAY ATTENTION HERE: Here we use the first function 
# we defined to create the first node.
# Start conversation with the LLM:
workflow.add_node("conversation", call_model)

# PAY ATTENTION HERE: Here we use the second function 
# we defined to create the second node.
# Summarize the conversation:
workflow.add_node(summarize_conversation)

# Set the entry point as conversation
workflow.add_edge(START, "conversation")

# PAY ATTENTION HERE: Here we use the third function 
# we defined to create a conditional edge.
# If there are more than six messages, go to Summarize the conversation:
workflow.add_conditional_edges("conversation", should_continue)
workflow.add_edge("summarize_conversation", END)

# PAY ATTENTION HERE: See how we add MemorySaver as checkpointer
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

model = ChatOpenAI(model="gpt-4o")

# PAY ATTENTION HERE: see how add the thread_id in the config
config = {"configurable": {"thread_id": "1"}}

# Our first message to the chatbot
input_message = HumanMessage(content="Hi! I'm Julio")

# PAY ATTENTION HERE: see how we include the config with the thread_id
output = graph.invoke({"messages": [input_message]}, config) 

# Prints the response from the chatbot
for m in output['messages'][-1:]:
    m.pretty_print()

# Our second message to the chatbot
input_message = HumanMessage(content="what's my name?")

# PAY ATTENTION HERE: see how we include the config with the thread_id
output = graph.invoke({"messages": [input_message]}, config) 

# Prints the response from the chatbot
for m in output['messages'][-1:]:
    m.pretty_print()

# Our third message to the chatbot
input_message = HumanMessage(content="I like the San Francisco Bay")

# PAY ATTENTION HERE: see how we include the config with the thread_id
output = graph.invoke({"messages": [input_message]}, config) 

# Prints the response from the chatbot
for m in output['messages'][-1:]:
    m.pretty_print()
    
# Our fourth message to the chatbot
input_message = HumanMessage(content="The city of San Francisco is not as friendly to live as it used to be")

# PAY ATTENTION HERE: see how we include the config with the thread_id
output = graph.invoke({"messages": [input_message]}, config) 

# Prints the response from the chatbot
for m in output['messages'][-1:]:
    m.pretty_print()

# PAY ATTENTION HERE: now we have 4 inputs and 4 outputs, 
# so in total we have 8 messages (4 inputs + 4 outputs)

graph.get_state(config).values.get("summary","")