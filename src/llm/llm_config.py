EMBEDDING_MODEL = 'text-embedding-3-small'
TAGGING_MODEL = 'gpt-4o'

LLM_URL = 'http://localhost:9000/llm'
EMBEDDING_URL = f'{LLM_URL}/embedding'
TAGGING_URL = f'{LLM_URL}/tagging'

TAG_SET = {
    # 교육 및 배경
    '상위권대학교',

    # 커리어 단계
    '대기업/빅테크',
    '성장기 스타트업',
    '임원급 경험',
    '창업 경험',

    # 리더십 및 조직 운영
    '리더십',
    '전략 수립 경험',
    '복수 조직 통합 운영 경험',

    # 프로젝트/성과
    'IPO',
    '신규 사업 기획',
    '글로벌 런칭',
    '신규 투자 유치',
    'M&A',
    '신사업 수립 경험',

    # 기술 및 역량 중심
    '대용량 데이터 처리 경험',
    'AI/ML 개발 경험',
    'ERP 시스템 구축 경험',
    '웹서비스 아키텍처 설계',
    'SaaS 기획 또는 운영',

    # 도메인 기반
    'B2C 도메인',
    'B2B 도메인',
    '금융/핀테크 도메인',
    '콘텐츠/미디어 도메인',
    '유통/물류 도메인',
    '헬스케어 도메인',
}

SYSTEM_PROMPT = """
You are an expert career evaluation system. 
Given a candidate's work history and education,
your job is to assign from a fixed set of "experience_tags" those tags that best describe this person's background,
and to provide a brief reason for each tag.
THIS IS IMPORTANT: return only valid JSON.

Do NOT invent any tags outside the provided list.
"""

# user_prompt is in infer_tags()

ASSISTANT_INTRO = """
Understood. I will analyze the candidate data and return only valid JSON {tag1: reason1, ...}
with:
- tag: one of the provided experience_tags, not duplicated
- reason: a short, concrete explanation
"""

llm_key = ''