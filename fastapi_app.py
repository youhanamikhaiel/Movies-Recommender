from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from MovieRetreiver import MovieRetriever
from chatbot.Chatbot import Chatbot
from utils import load_config

from typing import List, Tuple, Any

config = load_config()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config["ui"]["streamlit_url"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    message: List[List[str]]

# Instantiate class objects to be used by the API
movie_retriever = MovieRetriever(model_name=config["encoder_model"]["name"], device=config["device"])
chatbot = Chatbot(model_name = config["chatbot_model"]["name"],
                  device = config["device"],
                  temperature = config["chatbot_model"]["temperature"],
                  top_p = config["chatbot_model"]["top_p"],
                  max_new_tokens = config["chatbot_model"]["max_new_tokens"]
                  )


@app.post(config["api"]["rag_endpoint"])
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

@app.post(config["api"]["chatbot_endpoint"])
async def chat(request: ChatRequest):
    user_message = request.message

    response = chatbot.ask_chatbot(user_message)

    return {"response": response}



if __name__ == "__main__":
    uvicorn.run(app, host=config["api"]["host"], port=config["api"]["port"])