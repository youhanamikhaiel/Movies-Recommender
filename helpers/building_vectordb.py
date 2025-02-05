import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('dataset/movies_all_description.csv')

# Load the embedding model using LangChain
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", model_kwargs={'device': 'mps'})

persist_directory = "chroma_db"

vector_store = Chroma(collection_name="movie_descriptions",
                      embedding_function=embedding_model,
                     persist_directory=persist_directory)

documents = data['description'].tolist()
metadata = data[["id", "Title", "Year"]].to_dict(orient="records")

# Add documents with metadata
vector_store.add_texts(texts=documents, metadatas=metadata)

vector_store.persist()