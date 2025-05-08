from typing import List, cast

from fastapi import APIRouter, Request
from openai.types.chat import ChatCompletionMessageParam

from src.llm.llm_utils import InferRequest
from src.llm.llm_config import (
    EMBEDDING_MODEL,
    TAGGING_MODEL,
    TAG_SET,
    SYSTEM_PROMPT,
    ASSISTANT_INTRO
)

llm_router = APIRouter()


@llm_router.post('/llm/embedding')
async def response_to_embedding(data: InferRequest, request: Request):
    llm = request.app.state.llm
    response = await llm.embeddings.create(
        input=data.text,
        model=EMBEDDING_MODEL
    )

    return {'response': response}


@llm_router.post('/llm/tagging')
async def response_to_tag(data: InferRequest, request: Request):
    llm = request.app.state.llm
    user_prompt = f"""
        Please make tags from this, with the fixed tag set {TAG_SET};
            {data.text}
    """
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_prompt},
        {'role': 'assistant', 'content': ASSISTANT_INTRO}
    ]

    # form a json strictly
    functions = [{
        'name': 'return_tags',
        'description': 'Returns a JSON object mapping tags to short explanations.',
        'parameters': {
            'type': 'object',
            'properties': {
                'tags': {
                    'type': 'object',
                    'additionalProperties': {'type': 'string'}
                }
            },
            'required': ['tags']
        }
    }]

    response = await llm.chat.completions.create(
        messages = cast(
            List[ChatCompletionMessageParam],
            messages
        ),
        model=TAGGING_MODEL,
        functions=functions,
        function_call={'name': 'return_tags'},
        max_tokens=200,
        temperature=0.3
    )

    return {'response': response}
