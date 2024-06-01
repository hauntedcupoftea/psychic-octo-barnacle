"""all fastapi routers go here"""
from fastapi import APIRouter, Depends, status, HTTPException
from app.functions import *
from app.basemodels import *

qna = APIRouter(
    prefix='/qna',
    tags=['qna']
)

@qna.post('/luke-skywalker-wiki', status_code=status.HTTP_200_OK, response_model=QResponse)
def api_rag_skywalker(request: QQuery):
    return luke_skywalker_rag(request)