import os

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": os.getenv("POSTGRES_USER", "searchright"),
    "password": os.getenv("POSTGRES_PASSWORD", "searchright"),
    "database": os.getenv("POSTGRES_DB", "searchright"),
}

INDEX_TALENT_DB_PARAMS = {
    'ivfflat_lists': 100,
    'm': 16,
    'ef_construction': 200
}
