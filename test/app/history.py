from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[],
    checkpointer=InMemorySaver(),
)


config = {"configurable": {"thread_id": str(uuid7())}}

while True:
    query = input("> ")

    if query == "bye" or query == "exit":
        break

    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config,
    )

    print(result["messages"][-1].content_blocks[0]["text"])

