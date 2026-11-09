import json
import os
from typing import Annotated, TypedDict
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from gh import list_commits, get_commit, format_diff


# 1. Tools: the docstring is what the model reads to decide when to use it
@tool
def list_recent_commits(n: int = 3) -> str:
    """List the most recent commits (sha + first line of message)."""
    return json.dumps(list_commits(n))


@tool
def get_commit_diff(sha: str) -> str:
    """Get the full message and code diff for one commit by its sha."""
    c = get_commit(sha)
    return f"Message: {c['commit']['message']}\n\n{format_diff(c)}"


tools = [list_recent_commits, get_commit_diff]
llm = ChatGroq(model=os.environ.get(
    "GROQ_MODEL", "llama-3.3-70b-versatile")).bind_tools(tools)

SYSTEM = """You write tweets for a developer who builds in public.
Look at the recent commits, pick the most tweet-worthy one, read its diff,
then write ONE tweet under 280 characters (first person, casual, max 1 emoji,
max 2 hashtags, never include secrets).
If every commit is trivial (typos, formatting, merges), reply with exactly: SKIP
Output only the tweet text or SKIP."""


# 2. State: what the graph carries between steps
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 3. Node: one LLM call
def agent(state: State):
    reply = llm.invoke([SystemMessage(SYSTEM)] + state["messages"])
    return {"messages": [reply]}


# 4. Wire the graph
builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
# tool call? -> "tools", else -> END
builder.add_conditional_edges("agent", tools_condition)
# after tools, go back to the LLM
builder.add_edge("tools", "agent")
graph = builder.compile()

result = graph.invoke(
    {"messages": [HumanMessage("Write a tweet about my recent work.")]},
    {"recursion_limit": 10},  # step limit, like our `for step in range(8)`
)
print(result["messages"][-1].content)
