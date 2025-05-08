from typing import List, Dict, Optional, Union
import json

from pydantic import BaseModel, ValidationError
from fastapi import HTTPException


class PositionData(BaseModel):
    title: str
    companyName: str
    description: str
    startEndDate: Dict[str, Dict[str, int]]
    companyLocation: Optional[str] = None
    companyLogo: Optional[str] = None


class EducationData(BaseModel):
    schoolName: str
    fieldOfStudy: str
    originStartEndDate: Dict[str, Dict[str, int]]
    degreeName: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None
    startEndDate: Optional[str] = None


class TalentData(BaseModel):
    firstName: str
    lastName: str
    industryName: str
    skills: List[str]
    positions: List[PositionData]
    educations: List[EducationData]
    summary: Optional[str] = None
    headline: Optional[str] = None
    photoUrl: Optional[str] = None
    linkedinUrl: Optional[str] = None
    projects: Optional[List] = None
    website: Optional[List] = None
    recommendations: Optional[List] = None


# def validate_talent_data(contents: bytes) -> TalentData:
#     try:
#         talent_data = json.loads(contents)
#
#     except json.JSONDecodeError:
#         raise HTTPException(
#             status_code=400,
#             detail='Invalid JSON file'
#         )
#
#     try:
#         return TalentData(**talent_data)  # validated_data
#
#     except ValidationError as ve:
#         raise HTTPException(
#             status_code=422,
#             detail=ve.errors()
#         )


def validate_talent_data(payload: Union[bytes, Dict]) -> TalentData:
    if isinstance(payload, bytes):
        try:
            talent_data = json.loads(payload)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail='Invalid JSON file'
            )

    elif isinstance(payload, dict):
        talent_data = payload

    else:
        raise HTTPException(
            status_code=422,
            detail='Cannot read; expected JSON bytes or dict'
        )

    try:
        return TalentData(**talent_data)  # validated_data

    except ValidationError as ve:
        raise HTTPException(
            status_code=422,
            detail=ve.errors()
        )
