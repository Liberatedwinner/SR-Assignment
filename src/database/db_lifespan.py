import os
from contextlib import asynccontextmanager

from asyncpg import create_pool, Connection, PostgresError
from pgvector.asyncpg import register_vector
from fastapi import FastAPI

from src.database.sql_creates import CREATES_DICT
from src.database.db_config import DB_CONFIG, INDEX_TALENT_DB_PARAMS

IDX_M = INDEX_TALENT_DB_PARAMS['m']
IDX_EC = INDEX_TALENT_DB_PARAMS['ef_construction']


async def initialize_connection(connection: Connection):
    await register_vector(connection)


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    # add VECTOR type
    app.state.db_pool = await create_pool(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        init=initialize_connection
    )
    async with app.state.db_pool.acquire() as connection:
        try:
            # load extensions, just one time
            await connection.execute('CREATE EXTENSION IF NOT EXISTS vector;')
            await connection.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto;')

        except PostgresError as e:
            print('Cannot load extensions', e)

        try:
            # make a table from talent data
            # since the embedding part is using OpenAI embedding model,
            # the dimension of embedding is fixed
            await connection.execute(CREATES_DICT['talents'])

            # store raw_data
            await connection.execute(CREATES_DICT['raw_profiles'])

            # make 1:n tables
            # skills
            await connection.execute(CREATES_DICT['skills'])

            # positions
            await connection.execute(CREATES_DICT['positions'])

            # educations
            await connection.execute(CREATES_DICT['educations'])

            # embeddings and its vector index
            await connection.execute(CREATES_DICT['embeddings'][0])
            await connection.execute(CREATES_DICT['embeddings'][1])

            # tags
            await connection.execute(CREATES_DICT['tags'])

        except PostgresError as e:
            print('Cannot create tables', e)

    yield
    await app.state.db_pool.close()
