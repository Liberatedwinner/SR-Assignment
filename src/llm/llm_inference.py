from typing import Dict
import json

import numpy as np
from httpx import AsyncClient

from src.llm.llm_config import EMBEDDING_URL, TAGGING_URL
from src.api_config import TIMEOUT_LIMIT


async def get_embedding(text: str):
    """get normalized embedding"""

    async with AsyncClient(timeout=TIMEOUT_LIMIT) as client:
        try:
            response = await client.post(EMBEDDING_URL, json={'text': text})
            emb_json = response.json()
            raw_embedding = emb_json['response']['data'][0]['embedding']
            norm = np.linalg.norm(raw_embedding)
            if norm == 0:
                raise ValueError('Embedding has a zero norm')

            normalized = (np.array(raw_embedding) / norm).tolist()

            return {'status': 'ok', 'embedding': normalized}

        except Exception:
            raise


async def infer_tags(text: str) -> Dict[str, str]:

    async with AsyncClient(timeout=TIMEOUT_LIMIT) as client:
        try:
            response = await client.post(TAGGING_URL, json={'text': text})
            infer_json = response.json()
            try:
                content = infer_json['response'].choices[0].message
                if content.function_call and content.function_call.arguments:
                    arguments = json.loads(content.function_call.arguments)
                    tags = arguments['tags']

                else:
                    content = content.content or ''
                    try:
                        tags = json.loads(content)
                    except json.JSONDecodeError:
                        tags = {tag.strip(): '' for tag in content.split(',')}

                return tags

            except (AttributeError, KeyError):
                tags = infer_json['tags']

                return tags

        except Exception:
            raise
