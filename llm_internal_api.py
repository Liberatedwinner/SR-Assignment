import uvicorn
from fastapi import FastAPI

from src.llm.llm_lifespan import llm_lifespan
from src.routers.llm_router import llm_router

app = FastAPI(lifespan=llm_lifespan)
app.include_router(llm_router)


if __name__ == '__main__':
    uvicorn.run('llm_internal_api:app', host='127.0.0.1', port=9000)
