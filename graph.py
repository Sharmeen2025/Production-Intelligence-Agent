import os
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, SystemMessage
from dotenv import load_dotenv

# Import the tools we just built
from tools import web_search, calculate_metrics, query_database

load_dotenv()

# 1. The Core Memory Schema
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 2. Initialize Model & Bind Tools
tools = [web_search, calculate_metrics, query_database]
llm = ChatGroq(
    model_name="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)
# This physically attaches the tool schemas to the model
llm_with_tools = llm.bind_tools(tools)

# 3. Define the Reasoning Node
def agent_node(state: AgentState):
    # We inject a system prompt to give the agent its persona and instructions
    sys_msg = SystemMessage(content="You are AgentMatrix, an enterprise AI Agent. Use your tools to find accurate information or perform math. If a tool fails, analyze the error and try again.")
    
    # Combine system message with the conversation history
    messages = [sys_msg] + state["messages"]
    
    # The LLM reads the history and decides to either respond or call a tool
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 4. Build the State Machine Graph
workflow = StateGraph(AgentState)

# Add the "Reasoning" and "Action" nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools)) # ToolNode handles tool execution safely

# Define the execution flow
workflow.add_edge(START, "agent")

# Routing logic: If the LLM requests a tool, go to 'tools'. If it just talks, go to 'END'.
workflow.add_conditional_edges("agent", tools_condition)

# After a tool executes, ALWAYS return to the agent so it can read the result
workflow.add_edge("tools", "agent")

# Compile into a runnable application
agent_executor = workflow.compile()