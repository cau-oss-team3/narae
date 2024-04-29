from pydantic import BaseModel


class GPTRequest(BaseModel):
    """
    GPT request
    """

    interest: str
    session_details: str


class GPTResponse(BaseModel):
    """
    GPT response
    """

    response: str
