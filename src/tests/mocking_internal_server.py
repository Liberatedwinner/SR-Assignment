from typing import Dict
from fastapi import FastAPI, Request

app = FastAPI()


@app.post('/api')
async def api_mocking(request: Request) -> Dict:
    json_data = await request.json()
    return {
        'message': 'ok',
        'received': json_data
    }

