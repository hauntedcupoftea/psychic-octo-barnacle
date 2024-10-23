# psychic-octo-barnacle

> work of Anand Chauhan [![LinkedIn](https://img.icons8.com/?size=25&id=xuvGCOXi8Wyg)](https://www.linkedin.com/in/hauntedcupoftea/)

A wikipedia RAG application, that can parse one or multiple wiki pages and answer questions based on them. Currently being developed as a fun side-project over the summer of 2024.

## Instructions to run

1. Create an environment file. This file should be placed at `./data-and-utils/.env` (name exact) and must contain the following.

    ```env
    HF_TOKEN=<Your Huggingface Token (get from https://huggingface.co/settings/tokens)>
    API_URL=<The URL of the embedding model, I'm using 'https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2' but you can use anything>
    ```

2. Get an anaconda distro. I prefer [Mamba](https://github.com/conda-forge/miniforge) but you can use Conda also.

3. Create an environment with the specs in the `environment.yml` file (replace mamba with conda if using conda).

    ```bash
    mamba env create -f environment.yml
    ```

4. Activate the environment, and run the following command from the root directory of the project.

    ```bash
    fastapi run main_backend.py --port 8000
    ```

5. Go to localhost:8000/docs to test API Endpoints.
