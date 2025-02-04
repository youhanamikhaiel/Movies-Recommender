from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from MovieRetreiver import MovieRetriever


class QueryRequest(BaseModel):
    query: str


app = FastAPI()
movie_retriever = MovieRetriever()


@app.post("/search")
def search_movies(query_request: QueryRequest):
    # Perform the similarity search
    results = movie_retriever.search(query_request.query)
    # Format the results to a serializable list of dictionaries
    formatted_results = []
    for result, score in results:
        formatted_results.append({
            "title": result.metadata.get("Title", "Unknown"),
            "plot": result.page_content,
            "sim_score": 1 - score,
            "id": result.metadata.get("id", "Unknown")
        })
    return {"results": formatted_results}

if __name__ == "__main__":
    # Run the app with: uvicorn fastapi_app:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)