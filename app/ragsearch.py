import faiss
import numpy as np
import pandas as pd
from scrape import get_wikipedia_text, get_embeddings

class RAGSearcher:
    def __init__(self, urls: list[str]) -> None:
        self.text_corpus, self.faiss_db = self.create_vector_from_text(urls)
    
    def create_vector_from_text(self, urls: list[str] | str):
        # get text from all urls one by one
        text_corpus = []
        for url in urls:
            text_corpus.extend(get_wikipedia_text(url))
        text_embeddings = get_embeddings(text_corpus) 
        faiss_db = self.init_new_vector_database(text_embeddings, len(text_embeddings[0]), int(np.sqrt(len(text_embeddings)) / 4)) # can be changed later
        return text_corpus, faiss_db

    # TODO in the future: add a way to maybe save db's by conversation by person maybe? 
    # would need better CRUD for this
    def init_new_vector_database(self, embeddings: pd.Series, dims: int, nlist):
        quantizer = faiss.IndexFlatL2(dims)
        index = faiss.IndexIVFFlat(quantizer, dims, nlist) 
        # make it into a gpu index
        index.train(np.array(embeddings))
        index.add(np.array(embeddings))
        return index
    
    def search_faiss(self, query: str, k:int= 3):
        q_embed = np.array(get_embeddings([query])) # get embeddings from the model
        _dist, indices = self.faiss_db.search(q_embed, k)
        return [self.text_corpus[int(i)] for i in indices[0]]

if __name__ == "__main__":
    main = RAGSearcher(['https://en.wikipedia.org/wiki/Luke_Skywalker'])
    print(main.search_faiss("Why is Luke Skywalker Famous?"))