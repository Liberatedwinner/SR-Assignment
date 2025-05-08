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
