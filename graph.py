import os
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, SystemMessage
from dotenv import load_dotenv

from tools import web_search, calculate_metrics, query_database

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

tools = [web_search, calculate_metrics, query_database]

llm = ChatGroq(
    model_name="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

llm_with_tools = llm.bind_tools(tools)

def agent_node(state: AgentState):
    # Strict prompt to eliminate canned refusal responses
    system_instruction = (
        "You are the Production Intelligence Agent, an autonomous enterprise system with access to live external tools. "
        "You possess live internet connectivity through the 'web_search' tool and database access through 'query_database'. "
        "CRITICAL DIRECTIVE: NEVER claim you cannot access real-time data, stock prices, news, or current events. "
        "Whenever a user asks for current information, market data, or live facts, you MUST call the 'web_search' tool to retrieve the information. "
        "Execute tools autonomously to gather facts before providing your final answer."
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