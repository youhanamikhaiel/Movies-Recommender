# pylint: disable=missing-module-docstring

from langchain_ollama import ChatOllama

"""
Chatbot object that triggers the LLM to interacte with the user
"""

class Chatbot():
    def __init__(self, model_name="deepseek-r1:1.5b", temperature=0.6, top_p=0.9, max_new_tokens=1000, device = "mps"):
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_new_tokens = max_new_tokens
        self.device = device
        self.llm = ChatOllama(model="deepseek-r1:1.5b", device="mps", temperature=0.6, top_p=0.9, max_new_tokens=1000)

    def ask_chatbot(self, messages):
        ai_msg = self.llm.invoke(messages)
        return ai_msg.content.split("</think>\n\n")[1]
