"""All functions that will go into API calls go here"""
from fastapi import HTTPException, status
from transformers import pipeline
from app.scrape import query_llm
from app.ragsearch import RAGSearcher
from app.basemodels import QQuery, QResponse

# TODO, make this more modular and granular
def luke_skywalker_rag(request: QQuery, search=RAGSearcher):
    if request.query in [None, ""]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid query")
    main = search(['https://en.wikipedia.org/wiki/Luke_Skywalker'])
    query = "How many people has Luke Skywalker Killed?"
    context = main.search_faiss(query)
    pipe = pipeline("text2text-generation", model="google/flan-t5-small")
    llmres = query_llm(request.query, context, pipe)
    response = QResponse(
        query=request.query,
        relevant_chunks=context,
        answer=llmres[0]['generated_text']
    )
    return response

if __name__ == '__main__':
    # test
    print(luke_skywalker_rag(QQuery(query="Where was Luke Skywalker born?")))