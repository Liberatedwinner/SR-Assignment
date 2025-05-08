from typing import List, Dict, Optional, AsyncGenerator
from contextlib import asynccontextmanager
import hashlib
from uuid import UUID

from asyncpg import Connection
from pgvector.asyncpg import register_vector
from fastapi import Request

from src.api_utils import PositionData, EducationData, TalentData
from src.database.sql_inserts import INSERTS_DICT
from src.llm.llm_inference import get_embedding
from src.llm.llm_utils import build_embedding_text


def normalize_str(string: Optional[str]) -> str:
    return (string or '').strip().lower()


def compute_talent_hash(talent: TalentData) -> str:
    """for checking duplicates, compute a hash from the (nearly) unique value"""

    # linkedin url is unique
    # TODO: can use e-mail as a key?
    if talent.linkedinUrl:
        key = talent.linkedinUrl.strip().lower()
    else:
        col_to_key = ['firstName', 'lastName', 'headline', 'summary', 'industryName']
        key = '|'.join(
            normalize_str(getattr(talent, col))
            for col in col_to_key
        )

    return hashlib.sha256(key.encode()).hexdigest()


async def get_existing_id_by_hash(
        talent_hash: str, connection: Connection
) -> Optional[UUID]:
    existing_id = await connection.fetchval(
        'SELECT talent_id FROM talents WHERE talent_hash = $1',
        talent_hash
    )

    return existing_id


async def get_db_connection(request: Request) -> AsyncGenerator[Connection, None]:
    """yield Connection, return None"""
    db_pool = request.app.state.db_pool
    connection = await db_pool.acquire()
    await register_vector(connection)
    try:
        yield connection
    finally:
        await request.app.state.db_pool.release(connection)


# embedding
# TODO
async def load_talent_data(): ...


# for readability, divide insert functions
async def insert_positions(
        talent_id: UUID,
        positions: List[PositionData],
        connection: Connection
):
    for p in positions:
        p_args = [
            talent_id,
            p.title,
            p.companyName,
            p.companyLocation,
            p.description,
            p.startEndDate['start']['year'],
            p.startEndDate['start']['month'],
            p.startEndDate.get('end', {}).get('year'),
            p.startEndDate.get('end', {}).get('month')
        ]
        await connection.execute(
            INSERTS_DICT['positions'],
            *p_args
        )


async def insert_educations(
        talent_id: UUID,
        educations: List[EducationData],
        connection: Connection
):
    for e in educations:
        e_args = [
            talent_id,
            e.schoolName,
            e.degreeName,
            e.fieldOfStudy,
            e.originStartEndDate['startDateOn']['year'],
            e.originStartEndDate['startDateOn'].get('month'),
            e.originStartEndDate['endDateOn']['year'],
            e.originStartEndDate['endDateOn'].get('month')
        ]
        await connection.execute(
            INSERTS_DICT['educations'],
            *e_args
        )


async def insert_skills(
        talent_id: UUID,
        skills: List[str],
        connection: Connection
):
    for skill in skills:
        await connection.execute(
            INSERTS_DICT['skills'],
            talent_id, skill
        )


async def insert_raw_json(
        talent_id: UUID,
        raw_profiles: Dict,
        connection: Connection
):
    await connection.execute(
        INSERTS_DICT['raw_profiles'],
        talent_id, raw_profiles
    )


async def insert_embedding(
        talent_id: UUID,
        talent: TalentData,
        connection: Connection
):
    embedding_text = build_embedding_text(talent)
    embedding = await get_embedding(embedding_text)
    await connection.execute(
        INSERTS_DICT['embeddings'],
        talent_id, embedding
    )


async def insert_talent_to_db(
        talent: TalentData,
        connection: Connection
) -> UUID:
    talent_hash = compute_talent_hash(talent)
    existing_id = get_existing_id_by_hash(talent_hash, connection)

    if existing_id:
        talent_id = existing_id

    else:
        talent_id = ...
        async with connection.transaction():
            t_args = [
                talent_hash,
                talent.firstName,
                talent.lastName,
                talent.headline,
                talent.summary,
                talent.industryName,
                talent.linkedinUrl,
                talent.photoUrl,
                talent.projects,
                talent.website,
                talent.recommendations
            ]
            # insert and get talent_id
            talent_id = await connection.fetchval(
                INSERTS_DICT['talents'],
                *t_args
            )
            # store information
            await insert_positions(talent_id, talent.positions, connection)
            await insert_educations(talent_id, talent.educations, connection)
            await insert_skills(talent_id, talent.skills, connection)
            await insert_raw_json(talent_id, talent.model_dump(), connection)

            # store embedding
            await insert_embedding(talent_id, talent, connection)

    return talent_id


# store tags
async def insert_tags(
        talent_id: UUID,
        tags: Dict[str, str],
        connection: Connection
):
    """
    tags = {'tag1': 'reason1', ...}
    """
    for tag in tags.keys():
        await connection.execute(
            INSERTS_DICT['tags'],
            talent_id, tag
        )

