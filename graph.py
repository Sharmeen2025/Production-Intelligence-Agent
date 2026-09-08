import os
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, SystemMessage
from dotenv import load_dotenv

from tools import web_search, calculate_metrics, query_database, get_stock_price

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Add the new stock tool to the agent's arsenal
tools = [web_search, calculate_metrics, query_database, get_stock_price]

# Use the Llama 3.1 70B model, which is Groq's gold-standard for tool execution
llm = ChatGroq(
    model_name="llama-3.1-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

llm_with_tools = llm.bind_tools(tools)

def agent_node(state: AgentState):
    system_instruction = (
        "You are the Production Intelligence Agent. "
        "If the user asks for a stock price, YOU MUST use the 'get_stock_price' tool and provide the ticker symbol. "
        "Do not answer without using the tools."
    )
    sys_msg = SystemMessage(content=system_instruction)
    messages = [sys_msg] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent")

agent_executor = workflow.compile()