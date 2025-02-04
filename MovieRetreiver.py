from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

#disable warnings
import warnings
warnings.filterwarnings("ignore")


class MovieRetriever:
    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2", device = "mps"):
        self.embedding_model = HuggingFaceEmbeddings(model_name=model_name, model_kwargs={'device': device})
        self.vector_store = Chroma(persist_directory = "chroma_db",
                                  collection_name='movie_descriptions',
                                  embedding_function= self.embedding_model)
        
    def search(self, query, k=3):
        return self.vector_store.similarity_search_with_score(query, k=k)

"""
# Perform a similarity search
movie_retriever = MovieRetriever()

query = "a love story between a rich and poor"
results = movie_retriever.search(query)

# Display the results
for i, result in enumerate(results):
    print(f"Result {i + 1}:")
    print(f"  Title: {result[0].metadata['Title']}")
    print(f"  Description: {result[0].page_content}")
    print(f"  Similarity Score: {1-result[1]}")
    print()
"""