from typing import Dict, Union
from uuid import UUID

from httpx import HTTPError
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException

from src.api_utils import validate_talent_data
from src.database.db_utils import get_db_connection, insert_talent_to_db

router = APIRouter()


# def validate_talent_data(contents: bytes) -> TalentData:
#     try:
#         talent_data = json.loads(contents)
#
#     except json.JSONDecodeError:
#         raise HTTPException(
#             status_code=400,
#             detail='Invalid JSON file'
#         )
#
#     try:
#         return TalentData(**talent_data)  # validated_data
#
#     except ValidationError as ve:
#         raise HTTPException(
#             status_code=422,
#             detail=ve.errors()
#         )


@router.post('/upload-talents')
async def upload_talent(
        talent_file: UploadFile = File(...),
        connection=Depends(get_db_connection)
) -> Dict[str, Union[str, UUID]]:
    contents = await talent_file.read()
    validated_talent = validate_talent_data(contents)

    # talent_hash = compute_talent_hash(validated_talent)
    # talent_exists = await connection.fetchval(
    #     'SELECT talent_id FROM talents WHERE talent_hash = $1',
    #     talent_hash
    # )
    #
    # if talent_exists:
    #     raise HTTPException(
    #         status_code=409,
    #         detail='Duplicate talent data'
    #     )

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
