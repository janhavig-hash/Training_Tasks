from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    session_id: str = Field(..., min_length=1, description="The Session ID to filter documents") # <--- NEW FIELD