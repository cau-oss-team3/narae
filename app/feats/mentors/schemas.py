from pydantic import BaseModel, validator
from sqlalchemy import String, Integer


class STICC(BaseModel):
    situation: str
    task: str
    intent: str
    concern: str
    calibrate: str


class Mentor_Detail(BaseModel):
    mentor_name: str
    mentor_field: int
    mentor_sticc: STICC
