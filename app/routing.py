"""all fastapi routers go here"""
from fastapi import APIRouter

qna = APIRouter(
    prefix='/qna',
    tags=['qna']
)