from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: str

class InputsOfGPT(BaseModel):
    interest: str = "API design"
    session_details: str = "Recently, I tried to implement a new API using RESTful principles, but the data serialization is not efficient, and error handling is confusing."

class ItemSTICC(BaseModel):
    situation: str = "The problem i have faced is xxx."
    task: str = "To solve this problem, we have to do xxx."
    intent: str = "The reason for this is xxx."
    concerns: str = "But there is something that we must aware and be cautious."
    calibration: str = "Let's talk about things that we do not understand, or difficult, or we do not know, or should calibrate."