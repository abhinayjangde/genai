from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/chat",tags=["chat"])

class ChatRequest(BaseModel):
    query: str

@router.post("/")
async def chat(query: ChatRequest):

    return {
        "query": query.query,
        "message": "okay"
    }