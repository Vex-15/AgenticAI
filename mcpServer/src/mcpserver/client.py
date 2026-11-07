from dotenv import load_dotenv
from langchain.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

import asyncio

async def main():
    client = MultiServerMCPClient(
        {
            "main":{
                "command":"python",
                "args": ["\src\mcpserver\main.py"],
                "transport":"stdio"
            },
            "weather":{
                "url" : "http://127.0.0.1:8000/mcp",
                "transport" : "streamable_http"
            }
        }
    )

import os
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

tools = await client.get_tools()
model = ChatGroq(model="qwen-qwq-32b")
agent = create_react_agent(
    model, tools
)
