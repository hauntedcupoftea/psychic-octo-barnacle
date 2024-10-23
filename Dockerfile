FROM condaforge/miniforge3:latest

WORKDIR /app

COPY ./environment.yml /app/environment.yml

# Create the environment
RUN mamba env create -f environment.yml --yes --verbose

# Set the PATH to include the new environment
ENV PATH=/opt/conda/envs/psychic-octo-barnacle/bin:$PATH

COPY . .

# Run the FastAPI app within the new environment
CMD ["fastapi", "run", "main_backend.py", "--port", "8000"]
