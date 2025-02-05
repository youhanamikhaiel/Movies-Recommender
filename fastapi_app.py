from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from MovieRetreiver import MovieRetriever
from chatbot.Chatbot import Chatbot

from typing import List, Tuple, Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    message: List[List[str]]


movie_retriever = MovieRetriever()
chatbot = Chatbot()


@app.post("/search")
def search_movies(query_request: QueryRequest):
    results = movie_retriever.search(query_request.query)
    formatted_results = []
    for result, score in results:
        formatted_results.append({
            "title": result.metadata.get("Title", "Unknown"),
            "plot": result.page_content,
            "sim_score": 1 - score,
            "id": result.metadata.get("id", "Unknown")
        })
    return {"results": formatted_results}

@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message

    response = chatbot.ask_chatbot(user_message)

    return {"response": response}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)