from fastapi import FastAPI
from app.api.agent import router as agent_router

app = FastAPI()

app.include_router(agent_router, prefix="/api")