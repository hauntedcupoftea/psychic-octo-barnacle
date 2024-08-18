from bs4 import BeautifulSoup
from transformers import pipeline
import requests
import dotenv
import re
import logging

env = dotenv.dotenv_values('data-and-utils/.env')
logging.basicConfig(level=logging.INFO)

def split_into_sentences(text):
    # Split the text into sentences using a regular expression
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_endings.split(text)
    return sentences

def get_wikipedia_text(url: str, max_chunk_size: int = 500) -> list:
    try:
        page = requests.get(url)
        page.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve page: {e}")
        return []

    content = BeautifulSoup(page.content, 'html.parser')
    if not content:
        logging.error("Could not find main content div")
        return []

    chunks = []
    current_chunk = ""

    for element in content.find_all(['p', 'h2', 'h3', 'li']):
        if element.name in ['h2', 'h3']:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            chunks.append(element.text.strip())
        else:
            text = re.sub(r'\[.*?\]', '', element.text)  # Remove citation brackets
            text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
            
            if text:  # Only process non-empty text
                sentences = split_into_sentences(text)
                for sentence in sentences:
                    if len(sentence) > max_chunk_size:
                        # If a single sentence exceeds max_chunk_size, split it further
                        parts = [sentence[i:i + max_chunk_size] for i in range(0, len(sentence), max_chunk_size)]
                        chunks.extend(parts)
                    else:
                        chunks.append(sentence.strip())

    chunks = [chunk for chunk in chunks if chunk and not chunk.isspace() and len(chunk) > 20]

    if not chunks:
        logging.warning("No text chunks were extracted from the page")

    logging.info(f"Extracted {len(chunks)} chunks from {url}")
    return chunks

def get_embeddings(texts: list[str],  
                api_url:str=env['API_URL'], token:str=env['HF_TOKEN']):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options": {"wait_for_model": True}})
    return response.json()

def query_llm(query: str, context: list, pipe):
    prompt = f"Using the information: {' '.join(context)}, Answer the question: {query}"
    return pipe(prompt)

if __name__ == '__main__':
    from ragsearch import RAGSearcher
    import numpy as np
    print(get_wikipedia_text('https://en.wikipedia.org/wiki/Luke_Skywalker'))
    print(np.array(get_embeddings(['hello everybody my name is markiplier', 'and welcome back to another episode of five nights at freddys'])).shape)
    main = RAGSearcher(['https://en.wikipedia.org/wiki/Luke_Skywalker'])
    query = "How many people has Luke Skywalker Killed?"
    context = main.search_faiss(query)
    pipe = pipeline("text2text-generation", model="google/flan-t5-small")
    print(context, sep='\n')
    print(query_llm(query, context, pipe))