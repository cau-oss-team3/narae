from pydantic import BaseModel


class GPTRequest(BaseModel):
    """
    GPT request
    """

    interest: str = "API design"
    session_details: str = (
        "Recently, I tried to implement a new API using RESTful principles, but the data serialization is not efficient, and error handling is confusing."
    )


class GPTResponse(BaseModel):
    """
    GPT response
    """

    response: str
