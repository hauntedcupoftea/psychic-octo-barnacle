"""A collection of schemas that define json structures for API calling."""
from pydantic import BaseModel

class QnAQuery(BaseModel):
    query: str