import faiss as f
import pandas as pd
from scrape import get_wikipedia_text, get_embeddings

def create_vector_from_text(urls: list[str] | str):
    # get text from all urls one by one
    text_corpus = []
    for url in urls:
        text_corpus.extend(get_wikipedia_text(url))
    text_corpus = pd.Series(text_corpus) # convert to series for better indexing
    text_embeddings = get_embeddings(text_corpus) 
    faiss_db = init_new_vector_database(text_embeddings, len(text_embeddings[0]), 
                                        len(text_embeddings) // 50) # can be changed later
    return text_corpus, faiss_db

# TODO in the future: add a way to maybe save db's by conversation by person maybe? 
# would need better CRUD for this
def init_new_vector_database(embeddings: pd.Series, dims: int, nlist):
    quantizer = f.IndexFlatL2(dims)
    index = f.IndexIVFFlat(quantizer, dims, nlist)
    index.train(embeddings)
    index.add(embeddings)
    return index