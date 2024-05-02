from pydantic import BaseModel, validator
from sqlalchemy import String, Integer


class STICC(BaseModel):
    situation: str
    task: str
    intent: str
    concern: str
    calibrate: str


# TODO gpt API에 들어가는 모든 토큰에 대해 길이 제한 넣기 (413에러)
class Mentor_Detail(BaseModel):
    mentor_name: str
    mentor_field: int
    mentor_sticc: STICC
