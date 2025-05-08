import json
from unittest.mock import AsyncMock

import pytest

from src.llm.llm_inference import infer_tags



class DummyAsyncClient:
    def __init__(self, response):
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def post(self, url, json):
        return self._response


class DummyTagsResponseSimple:
    def __init__(self, tags):
        # infer_tags now expects a top-level {'tags': {...}}
        self._json = {'tags': tags}
    def json(self):
        return self._json

@pytest.mark.asyncio
async def test_infer_tags_simple_json(monkeypatch):
    tags_input = {'A': 'a', 'B': 'b'}
    dummy = DummyTagsResponseSimple(tags_input)
    client = DummyAsyncClient(dummy)
    monkeypatch.setenv('TAGGING_URL', 'http://fake')
    monkeypatch.setenv('TIMEOUT_LIMIT', '5')
    monkeypatch.setattr('src.llm.llm_inference.AsyncClient', lambda timeout: client)

    result = await infer_tags("sample text")
    assert result == tags_input

# class DummyTagsResponse:
#     def __init__(self, tags):
#         args = {'tags': tags}
#         self._json = {'tags': tags}
#         # self._json = {'response': {'data': [], 'choices': []}}
#         # self._json['response'] = {
#         #     'data': [],
#         #     'choices': [
#         #         {
#         #             'message': {
#         #                 'function_call': {'arguments': json.dumps(args)},
#         #                 'content': None
#         #             }
#         #         }
#         #     ]
#         # }
#     def json(self):
#         return self._json
#
# @pytest.mark.asyncio
# async def test_infer_tags_function_call(monkeypatch):
#     dummy = DummyTagsResponse({'A': 'a', 'B': 'b'})
#     client = DummyAsyncClient(dummy)
#     monkeypatch.setenv('TAGGING_URL', 'http://fake')
#     monkeypatch.setenv('TIMEOUT_LIMIT', '5')
#     monkeypatch.setattr('src.llm.llm_inference.AsyncClient', lambda timeout: client)
#
#
#     result = await infer_tags("sample text")
#     assert result == {'A': 'a', 'B': 'b'}