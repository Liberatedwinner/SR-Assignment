from unittest.mock import AsyncMock

import numpy as np
import pytest

from src.llm.llm_inference import get_embedding


class DummyResponse:
    def __init__(self, embedding):
        self._json = {'response': {'data': [{'embedding': embedding}]}}

    def json(self):
        return self._json

class DummyAsyncClient:
    def __init__(self, response):
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def post(self, url, json):
        return self._response

@pytest.mark.asyncio
async def test_get_embedding_normalization(monkeypatch):
    # Set up dummy normalized vector [3,4] -> norm=5 -> normalized [0.6,0.8]
    dummy = DummyResponse([3, 4])
    client = DummyAsyncClient(dummy)
    monkeypatch.setenv('EMBEDDING_URL', 'http://fake')
    monkeypatch.setenv('TIMEOUT_LIMIT', '5')
    # Patch AsyncClient to our dummy
    monkeypatch.setattr('src.llm.llm_inference.AsyncClient', lambda timeout: client)

    result = await get_embedding("hello")
    assert result['status'] == 'ok'
    emb = result['embedding']
    assert pytest.approx(np.linalg.norm(emb), rel=1e-6) == 1.0

@pytest.mark.asyncio
async def test_get_embedding_zero_vector(monkeypatch):
    dummy = DummyResponse([0, 0, 0])
    client = DummyAsyncClient(dummy)
    monkeypatch.setenv('EMBEDDING_URL', 'http://fake')
    monkeypatch.setenv('TIMEOUT_LIMIT', '5')
    monkeypatch.setattr('src.llm.llm_inference.AsyncClient', lambda timeout: client)

    with pytest.raises(ValueError):
        await get_embedding("empty")


# class DummyEmbedResp:
#     def __init__(self, vec):
#         self.data = [type('D', (), {'embedding': vec})]
#
# @pytest.mark.asyncio
# async def test_get_embedding_normalization(monkeypatch):
#     dummy = DummyEmbedResp([6, 8])  # norm should become 1
#     mock_client = AsyncMock()
#     mock_client.embeddings.create.return_value = dummy
#     monkeypatch.setattr('src.llm.llm_inference.AsyncClient', mock_client)
#
#     emb = await get_embedding("hello")
#     assert pytest.approx(np.linalg.norm(emb), rel=1e-6) == 1.0
#
# @pytest.mark.asyncio
# async def test_get_embedding_zero_vector(monkeypatch):
#     dummy = DummyEmbedResp([0, 0, 0])
#     mock_client = AsyncMock()
#     mock_client.embeddings.create.return_value = dummy
#     monkeypatch.setattr('src.llm.llm_inference.AsyncClient', mock_client)
#
#     with pytest.raises(ValueError):
#         await get_embedding("empty")
