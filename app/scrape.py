from bs4 import BeautifulSoup
from transformers import pipeline
import requests
import dotenv
import transformers

env = dotenv.dotenv_values('data-and-utils/.env')

def get_wikipedia_text(url: str) -> Exception | list:
    page = requests.get(url)
    if page.status_code != 200:
        return Exception("Page couldn't be downloaded!", page.content)
    wikisoup = BeautifulSoup(page.content, 'html.parser')
    content = wikisoup.find('div', attrs={
        'class' : "mw-content-ltr mw-parser-output"},
                            ) # find parser output (article content basically)
    chunks = []
    for child in content.children:
        if "References" in child.text:
            break
        chunks.extend([i.replace('\\', '') for i in child.text.split('\n') if i not in ['.mw', '\n', '']])
    return chunks

def get_embeddings(texts: list[str],  
                api_url:str=env['API_URL'], token:str=env['HF_TOKEN']):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options": {"wait_for_model": True}})
    return response.json()

def query_llm(query: str, context: list, pipe):
    prompt = f"Using the information: {' '.join(context)}, Answer the question {query}"
    return pipe(prompt)

if __name__ == '__main__':
    from ragsearch import RAGSearcher
    main = RAGSearcher(['https://en.wikipedia.org/wiki/Luke_Skywalker'])
    query = "Who is Luke Skywalker's teacher?"
    context = main.search_faiss(query)
    pipe = pipeline("text2text-generation", model="google/flan-t5-small")
    print(context, sep='\n')
    print(query_llm(query, context, pipe))