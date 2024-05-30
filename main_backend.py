from fastapi import FastAPI
from app.routing import rag, llm

app = FastAPI()

app.include_router(rag)
app.include_router(llm)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port='8000')