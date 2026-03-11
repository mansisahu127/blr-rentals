from fastapi import APIRouter

# 1. You must define the variable named 'router'
router = APIRouter() 

@router.post("/chat")
async def chat_endpoint():
    return {"message": "Hello from chat"}