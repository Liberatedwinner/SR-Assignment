INSERT_TALENTS = """
INSERT INTO talents (
    talent_hash,
    first_name,
    last_name,
    headline,
    summary,
    industry_name,
    linkedin_url,
    photo_url,
    projects,
    website,
    recommendations
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
RETURNING talent_id;
"""

INSERT_RAW_PROFILES = """
INSERT INTO talent_raw_profiles (talent_id, raw_profile)
VALUES ($1, $2);
"""

INSERT_SKILLS = """
INSERT INTO talent_skills (talent_id, skill)
VALUES ($1, $2);
"""

INSERT_POSITIONS = """
INSERT INTO talent_positions (
    talent_id,
    title,
    company_name,
    company_location,
    description,
    start_year,
    start_month,
    end_year,
    end_month
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9);
"""

INSERT_EDUCATIONS = """
INSERT INTO talent_educations (
    talent_id,
    school_name,
    degree_name,
    field_of_study,
    start_year,
    start_month,
    end_year,
    end_month
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
"""

INSERT_EMBEDDINGS = """
INSERT INTO talent_embeddings (talent_id, embedding)
VALUES ($1, $2);
"""

INSERT_TAGS = """
INSERT INTO talent_tags (talent_id, tag)
VALUES ($1, $2);
"""

INSERTS_DICT = {
    'talents': INSERT_TALENTS,
    'raw_profiles': INSERT_RAW_PROFILES,
    'skills': INSERT_SKILLS,
    'positions': INSERT_POSITIONS,
    'educations': INSERT_EDUCATIONS,
    'embeddings': INSERT_EMBEDDINGS,
    'tags': INSERT_TAGS
}