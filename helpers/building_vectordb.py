import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from utils import load_config 

config = load_config()

data = pd.read_csv('dataset/movies_all_description.csv')

# Load the embedding model using LangChain
embedding_model = HuggingFaceEmbeddings(model_name=config["encoder_model"]["name"], model_kwargs={'device': config["device"]})

vector_store = Chroma(collection_name=config["encoder_model"]["collection_name"],
                      embedding_function=embedding_model,
                      persist_directory=config["data"]["persist_directory"])

documents = data['description'].tolist()
metadata = data[["id", "Title", "Year"]].to_dict(orient="records")

# Add documents with metadata
vector_store.add_texts(texts=documents, metadatas=metadata)

vector_store.persist()
