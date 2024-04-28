from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str

class InputsOfGPT(BaseModel):
    interest: str = "API design"
    session_details: str = "Recently, I tried to implement a new API using RESTful principles, but the data serialization is not efficient, and error handling is confusing."
