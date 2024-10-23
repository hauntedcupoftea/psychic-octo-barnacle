"""All functions that will go into API calls go here"""
from fastapi import HTTPException, status
from transformers import pipeline, Pipeline
from app.scrape import query_llm
from app.ragsearch import RAGSearcher
from app.basemodels import QQuery, QResponse

def init_skywalker_rag():
    luke_skywalker_searcher = RAGSearcher(['https://en.wikipedia.org/wiki/Luke_Skywalker'])
    llm_pipe = pipeline("text2text-generation", model="google/flan-t5-small", device="cuda", max_new_tokens=64)
    return luke_skywalker_searcher, llm_pipe

def luke_skywalker_rag(request: QQuery, searcher: RAGSearcher, llm_pipe: Pipeline):
    if request.query in [None, ""]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid query")
    context = searcher.search_faiss(request.query, k=5)
    llmres = query_llm(request.query, context, llm_pipe)
    response = QResponse(
        query=request.query,
        relevant_chunks=context,
        answer=llmres[0]['generated_text']
    )
    return response

if __name__ == '__main__':
    # timed test for efficiency
    import time
    t0 = time.time()
    lss, llm = init_skywalker_rag()
    t1 = time.time()
    print(luke_skywalker_rag(QQuery(query="Where was Luke Skywalker born?"), lss, llm))
    t2 = time.time()
    print(luke_skywalker_rag(QQuery(query="Who did Luke Skywalker marry?"), lss, llm))
    t3 = time.time()
    print(f"""
    Testing report:
    - time taken by init function: {t1-t0}
    - time taken by first query: {t2-t1}
    - time taken by second query: {t3-t2}
    """)