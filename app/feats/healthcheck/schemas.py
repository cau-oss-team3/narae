from pydantic import BaseModel

class PingResponseSchema(BaseModel):
    message: str = 'pong'
