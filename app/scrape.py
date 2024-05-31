from bs4 import BeautifulSoup
import transformers
import torch
import requests
import dotenv

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

def query_llama(query: str, model_id:str=env['LLM_ID']):
    pipeline = transformers.pipeline("text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, 
                                    use_auth_token=env['HF_TOKEN'], device_map="auto")
    return pipeline(query)

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Luke_Skywalker'
    content = get_wikipedia_text(url)
    print(content, sep='\n')
    embeddings = get_embeddings(content)
    print(str(len(embeddings)) + ', ' + str(len(embeddings[0])))
    print(query_llama("Hey how are you doing today?"))