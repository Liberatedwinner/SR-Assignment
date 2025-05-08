from contextlib import asynccontextmanager

from fastapi import FastAPI
from openai import AsyncOpenAI

from src.llm.llm_config import llm_key


@asynccontextmanager
async def llm_lifespan(app: FastAPI):
    # initialize LLM core
    app.state.llm = AsyncOpenAI(api_key=llm_key)
    yield
