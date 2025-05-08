import uvicorn
from fastapi import FastAPI

from src.database.db_lifespan import db_lifespan
from src.routers import talent_search, talent_upload, tag_extraction
from src.api_config import DB_PREFIX, INFER_PREFIX


app = FastAPI(lifespan=db_lifespan)

# for search
app.include_router(talent_search.router, prefix=DB_PREFIX)

# for upload to DB
app.include_router(talent_upload.router, prefix=DB_PREFIX)

# for tag inference
app.include_router(tag_extraction.app_router, prefix=INFER_PREFIX)

# # for tag inference, without saving to DB
# app.include_router(tag_extraction.llm_router, prefix=INFER_PREFIX)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
