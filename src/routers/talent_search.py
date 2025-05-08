from pydantic import BaseModel
from fastapi import APIRouter, Depends

from src.database.db_utils import get_db_connection
from src.llm.llm_inference import get_embedding

router = APIRouter()


class SearchQuery(BaseModel):
    query: str
    top_k: int = 3


@router.post('/search-talents')
async def search_talents(
        query: SearchQuery,
        connection=Depends(get_db_connection)
):
    select_talents = """
    SELECT talent_id, embedding <=> $1 AS cos_distance
    FROM talent_embeddings
    ORDER BY cos_distance
    LIMIT $2;
    """
    collect_positions = """
    SELECT *
    FROM talent_positions
    WHERE talent_id = ANY($1)
    ORDER BY talent_id
    """

    try:
        query_embedding = await get_embedding(query.query)
        similar_rows = await connection.fetch(
            select_talents,
            query_embedding,
            query.top_k
        )
        similar_ids = [row['talent_id'] for row in similar_rows]
        position_rows = await connection.fetch(
            collect_positions,
            similar_ids
        )
        position_information = {{
            'talent_id': t_id,
            'positions': [dict(row) for row in position_rows if row['talent_id'] == id]
        } for t_id in similar_ids}

        return {'status': 'ok', 'information': position_information}

    except Exception:
        raise

