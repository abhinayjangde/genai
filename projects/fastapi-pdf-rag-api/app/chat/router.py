from fastapi import APIRouter
from pydantic import BaseModel
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

router = APIRouter(prefix="/chat",tags=["chat"])

class ChatRequest(BaseModel):
    query: str

agent = create_agent(
    model="google_genai:gemini-3.7-flash",
    tools=[],
    system_prompt="You are a helpful assistant",
)


@router.post("/")
async def chat(query: ChatRequest):
    result = agent.invoke(
    {"messages": [{"role": "user", "content": query.query}]}
)
    print(result["messages"][-1].content_blocks)
    return {
        "query": query.query,
        "response": result["messages"][-1].content_blocks
    }