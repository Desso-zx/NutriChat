from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """What the frontend sends us: just a question."""
    question: str = Field(
        ...,
        min_length=1,
        description="The user's nutrition question",
    )

class QueryResponse(BaseModel):
    """What we send back: the answer plus which documents it came from."""
    answer: str
    sources: list[str]