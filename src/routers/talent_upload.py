from typing import Dict, Union
from uuid import UUID

from httpx import HTTPError
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException

from src.api_utils import validate_talent_data
from src.database.db_utils import get_db_connection, insert_talent_to_db

router = APIRouter()


@router.post('/upload-talents')
async def upload_talent(
        talent_file: UploadFile = File(...),
        connection=Depends(get_db_connection)
) -> Dict[str, Union[str, UUID]]:
    contents = await talent_file.read()
    validated_talent = validate_talent_data(contents)

    try:
        talent_id = await insert_talent_to_db(
            validated_talent, connection
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

    return {'status': 'ok', 'talent_id': talent_id}
