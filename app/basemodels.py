"""A collection of schemas that define json structures for API calling."""
from typing import List
from pydantic import BaseModel, Field

class QQuery(BaseModel):
    query: str = Field(examples=['Who is Luke Skywalker?', 'Who plays Luke Skywalker?'])

class QResponse(BaseModel):
    query: str = Field(examples=['Where was Luke Skywalker born?'])
    relevant_chunks: List[str] = Field(examples=[['Chunk 1', 'Chunk 2', 'Chunk 3']])
    answer: str = Field(examples=['Tatooine'])