from src.database.db_config import INDEX_TALENT_DB_PARAMS

IDX_M = INDEX_TALENT_DB_PARAMS['m']
IDX_EC = INDEX_TALENT_DB_PARAMS['ef_construction']


CREATE_TALENTS_TABLE = """
CREATE TABLE IF NOT EXISTS talents (
    talent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    talent_hash TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    headline TEXT,
    summary TEXT,
    industry_name TEXT,
    linkedin_url TEXT,
    photo_url TEXT,
    projects JSONB DEFAULT '[]'::JSONB,
    website TEXT[] DEFAULT ARRAY[]::TEXT[],
    recommendations JSONB DEFAULT '[]'::JSONB,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
"""

CREATE_RAW_PROFILES_TABLE = """
CREATE TABLE IF NOT EXISTS talent_raw_profiles (
    talent_id UUID PRIMARY KEY REFERENCES talents(talent_id) ON DELETE CASCADE,
    raw_profile JSONB NOT NULL
);
"""

CREATE_SKILLS_TABLE = """
CREATE TABLE IF NOT EXISTS talent_skills (
    talent_id UUID REFERENCES talents(talent_id) ON DELETE CASCADE,
    skill TEXT,
    PRIMARY KEY (talent_id, skill)
);
"""

CREATE_POSITIONS_TABLE ="""
CREATE TABLE IF NOT EXISTS talent_positions (
    position_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    talent_id UUID REFERENCES talents(talent_id) ON DELETE CASCADE,
    title TEXT,
    company_name TEXT,
    company_location TEXT,
    description TEXT,
    start_year INT,
    start_month INT,
    end_year INT,
    end_month INT
);
"""

CREATE_EDUCATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS talent_educations (
    education_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    talent_id UUID REFERENCES talents(talent_id) ON DELETE CASCADE,
    school_name TEXT,
    degree_name TEXT,
    field_of_study TEXT,
    start_year INT,
    start_month INT,
    end_year INT,
    end_month INT
);
"""

CREATE_EMBEDDINGS_TABLE = """
CREATE TABLE IF NOT EXISTS talent_embeddings (
    embedding_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    talent_id UUID REFERENCES talents(talent_id) ON DELETE CASCADE,
    embedding VECTOR(1536),
    updated_at TIMESTAMPTZ DEFAULT now()
);
"""

CREATE_VECTOR_INDEX_ON_EMB = f"""
CREATE INDEX IF NOT EXISTS index_embedding_vector
ON talent_embeddings
USING hnsw (embedding vector_cosine_ops)
WITH (m = {int(IDX_M)}, ef_construction = {int(IDX_EC)});
"""

CREATE_TAGS_TABLE = """
CREATE TABLE IF NOT EXISTS talent_tags (
    talent_id UUID REFERENCES talents(talent_id) ON DELETE CASCADE,
    tag TEXT,
    updated_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (talent_id, tag)
);
"""

CREATES_DICT = {
    'talents': CREATE_TALENTS_TABLE,
    'raw_profiles': CREATE_RAW_PROFILES_TABLE,
    'skills': CREATE_SKILLS_TABLE,
    'positions': CREATE_POSITIONS_TABLE,
    'educations': CREATE_EDUCATIONS_TABLE,
    'embeddings': [CREATE_EMBEDDINGS_TABLE, CREATE_VECTOR_INDEX_ON_EMB],
    'tags': CREATE_TAGS_TABLE
}