import json
from typing import Dict

from httpx import ConnectError, ReadTimeout
from asyncpg.exceptions import UniqueViolationError, PostgresError
from pydantic import BaseModel
from fastapi import APIRouter, Depends, UploadFile, HTTPException, BackgroundTasks

from src.api_utils import validate_talent_data
from src.database.db_utils import (
    compute_talent_hash,
    get_existing_id_by_hash,
    get_db_connection,
    insert_talent_to_db,
    insert_tags
)
from src.llm.llm_inference import infer_tags
from src.llm.llm_utils import build_embedding_text

app_router = APIRouter()
llm_router = APIRouter()


class TalentRequest(BaseModel):
    talent_file: UploadFile
    talent_data: Dict


@app_router.post('/extract-tags')
async def extract_tags(
        request: TalentRequest,
        background_tasks: BackgroundTasks,
        connection=Depends(get_db_connection)
):
    """infer tags -> store them to DB"""

    if request.talent_file:
        payload = await request.talent_file.read()
    elif request.talent_data:
        payload = request.talent_data
    else:
        raise HTTPException(status_code=422, detail='need a file or json')

    talent = validate_talent_data(payload)
    talent_hash = compute_talent_hash(talent)
    existing_id = get_existing_id_by_hash(talent_hash, connection)

    if existing_id:
        talent_id = existing_id
    else:
        talent_id = await insert_talent_to_db(talent, connection)

    try:
        embedding_text = build_embedding_text(talent)
        # tags = await infer_tags(talent)
        tags = await infer_tags(embedding_text)
    except json.JSONDecodeError:
        raise HTTPException(
            502,
            detail='Invalid response from inference LLM'
        )
    except ConnectError:
        raise HTTPException(
            503,
            detail='Cannot connect to inference LLM'
        )
    except ReadTimeout:
        raise HTTPException(
            504,
            detail='Inference LLM timed out'
        )
    except Exception:
        raise HTTPException(
            500,
            detail='Internal server error'
        )

    def _save_tags():
        try:
            insert_tags(talent_id, tags, connection)
        except UniqueViolationError as u:
            raise HTTPException(
                502,
                detail=f'{u}|Duplicate tags for talent_id={talent_id}'
            )
        except PostgresError as p:
            raise HTTPException(
                500,
                detail=f'{p}|Postgres error storing tags for talent_id={talent_id}'
            )
        except Exception:
            raise HTTPException(
                500,
                detail=f'Unexpected error storing tags for talent_id={talent_id}'
            )

    background_tasks.add_task(_save_tags)

    return {'status': 'ok', 'talent_id': talent_id, 'tags': tags}


@llm_router.post('/extract-tag-directly')
async def extract_tags_without_db():
    """infer tags without saving to DB"""
    ...
