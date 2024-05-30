"""all fastapi routers go here"""
from fastapi import APIRouter

rag = APIRouter(
    prefix='/rag',
    tags=['rag']
)

llm = APIRouter(
    prefix='/llm',
    tags=['llm']
)