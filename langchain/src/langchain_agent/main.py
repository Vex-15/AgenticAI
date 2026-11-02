
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

@tool
def search(city: str) -> str:
    """Search for hotels in the city."""
    return f"Found hotels in {city}: Hotel A, Hotel B, Hotel C"


model = ChatOpenAI(temperature=0, model="gpt-4o-mini")

agent = create_agent(
    model=model,
    tools=[search],
    checkpointer=MemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model=model,
            trigger=("fraction", 0.005),
            keep=("fraction", 0.01),
        )
    ],
)

config = {"configurable": {"thread_id": "test-1"}}

cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]


def count_tokens(messages):
    return sum(len(str(m.content)) for m in messages) // 4


for city in cities:
    response = agent.invoke(
        {"messages": [HumanMessage(content=f"Search for hotels in {city}")]},
        config=config,
    )

    messages = response["messages"]
    tokens = count_tokens(messages)
    fraction = tokens / 128000

    print(f"City: {city}, Tokens: {tokens}, Fraction: {fraction:.6f}")
    print(messages)
