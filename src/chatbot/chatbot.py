# pylint: disable=missing-module-docstring

from langchain_ollama import ChatOllama


class Chatbot():
    """
    Chatbot class that triggers the LLM to interacte with the user
    """
    def __init__(self, model_name="deepseek-r1:1.5b", temperature=0.6, top_p=0.9, max_new_tokens=1000, device = "mps"):
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_new_tokens = max_new_tokens
        self.device = device
        self.llm = ChatOllama(model=self.model_name,
                              device=self.device,
                              temperature=self.temperature,
                              top_p=self.top_p,
                              max_new_tokens=self.max_new_tokens)

    def ask_chatbot(self, messages):
        ai_msg = self.llm.invoke(messages)
        return ai_msg.content.split("</think>\n\n")[1]
