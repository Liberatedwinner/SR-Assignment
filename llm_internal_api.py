# from typing import List, cast
import uvicorn
from fastapi import FastAPI, Request
# from openai.types.chat import ChatCompletionMessageParam

from src.llm.llm_lifespan import llm_lifespan
# from llm_utils import InferRequest
# from llm_config import (
#     EMBEDDING_MODEL,
#     TAGGING_MODEL,
#     TAG_SET,
#     SYSTEM_PROMPT,
#     ASSISTANT_INTRO
# )
from src.routers.llm_router import llm_router

app = FastAPI(lifespan=llm_lifespan)
app.include_router(llm_router)


# @app.post('/llm/embedding')
# async def response_to_embedding(data: InferRequest, request: Request):
#     llm = request.app.state.llm
#     response = await llm.embeddings.create(
#         input=data.text,
#         model=EMBEDDING_MODEL
#     )
#
#     return {'response': response}


# @app.post('/llm/tagging')
# async def response_to_tag(data: InferRequest, request: Request):
#     llm = request.app.state.llm
#     user_prompt = f"""
#         Please make tags from this, with the fixed tag set {TAG_SET};
#             {data.text}
#     """
#     messages = [
#         {'role': 'system', 'content': SYSTEM_PROMPT},
#         {'role': 'user', 'content': user_prompt},
#         {'role': 'assistant', 'content': ASSISTANT_INTRO}
#     ]
#
#     response = await llm.chat.completions.create(
#         messages = cast(
#             List[ChatCompletionMessageParam],
#             messages
#         ),
#         model=TAGGING_MODEL,
#         max_tokens=200,
#         temperature=0.3
#     )
#
#     return {'response': response}


if __name__ == '__main__':
    uvicorn.run('llm_internal_api:app', host='127.0.0.1', port=9000)
