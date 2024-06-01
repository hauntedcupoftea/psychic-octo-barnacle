from fastapi import FastAPI
from app.routing import qna

app = FastAPI(
    title='psychic-octo-barnacle', 
    version='0.2.0'
)

app.include_router(qna)

@app.get('/')
def health():
    return {
        "message" : "Welcome to the Wikipedia Rag-Searching API!"
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app=app, 
        port=8000,
    )