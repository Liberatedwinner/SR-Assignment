from pydantic import BaseModel

from src.api_utils import TalentData


class InferRequest(BaseModel):
    text: str

def build_embedding_text(talent: TalentData) -> str:
    positions = [
        f'{p.title} at {p.companyName}: {p.description}'
        for p in talent.positions
    ]
    positions_text = ','.join(positions)

    educations = [f'{e.schoolName}' for e in talent.educations]
    educations_text = ','.join(educations)

    return f'work experiences: {positions_text} | educations: {educations_text}'


# async def get_embedding(text: str) -> List[float]:
#     """get normalized embedding"""
#     response = await emb_core.embeddings.create(
#         input=text,
#         model=EMBEDDING_MODEL
#     )
#     raw_embedding = response['data'][0]['embedding']
#     norm = np.linalg.norm(raw_embedding)
#     if norm == 0:
#         raise ValueError('Embedding has a zero norm')
#
#     normalized = (np.array(raw_embedding) / norm).tolist()
#
#     return normalized
