from typing import Dict
import json
import uvicorn
from httpx import AsyncClient, ConnectError, ReadTimeout, HTTPError
from pydantic import ValidationError
from fastapi import FastAPI, File, UploadFile, HTTPException

from src.api_utils import TalentData
from src.api_config import TIMEOUT_LIMIT

URL = 'http://localhost:9000/api'  # TEMP
app = FastAPI()


@app.post('/talent')
async def load_talent_data(talent_file: UploadFile = File(...)) -> Dict:
    try:
        contents = await talent_file.read()
        talent_data = json.loads(contents)
        validated_data = TalentData(**talent_data)

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail='Invalid JSON file')

    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())

    async with AsyncClient(timeout=TIMEOUT_LIMIT) as client:
        try:
            response = await client.post(URL, json=validated_data.model_dump())
            status_code = response.status_code

            if status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail=f'Internal server returned <{status_code}: {response.text}>'
                )

            return {
                'status': 'ok',
                'internal_response': response.json()
            }

        except ConnectError:
            raise HTTPException(
                status_code=503,
                detail='Cannot connect to LLM'
            )

        except ReadTimeout:
            raise HTTPException(
                status_code=504,
                detail=f'Timeout occurred while waiting for LLM response; limit: {TIMEOUT_LIMIT}'
            )

        except HTTPError as e:
            raise HTTPException(
                status_code=500,
                detail=f'HTTP error: {str(e)}'
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Unexpected error: {str(e)}'
            )


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=1234, reload=True)
