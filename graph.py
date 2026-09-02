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
    # Strict prompt with a circuit breaker to prevent infinite loops
    system_instruction = (
        "You are the Production Intelligence Agent, an autonomous enterprise system. "
        "1. If a user asks for real-time data, stock prices, or news, you MUST use the 'web_search' tool. "
        "2. CRITICAL: Once you receive the tool's output, you must synthesize the final answer immediately. DO NOT call the tool again for the same query."
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