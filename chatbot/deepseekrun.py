import time
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage



llm = ChatOllama(model="deepseek-r1:1.5b", device="mps", temperature=0.6, top_p=0.9, max_new_tokens=1000)

messages = [
    ("system",
     "Please provide a short answer to this question: Explain the concept of reinforcement learning.")
    ]


ai_msg = llm.invoke(messages)
print(ai_msg.content.split("</think>\n\n")[1])

"""
# Move model to MPS
device = torch.device("mps")

model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.to(device)

messages = [
    {"role": "user", "content": "Please provide a short answer to this question: Explain the concept of reinforcement learning."},
]
"""


"""
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device="mps")
start_time = time.time()
output = pipe(messages, max_new_tokens=1000, temperature=0.6, top_p=0.9)
o_answer = output[0]["generated_text"][1]["content"].split("</think>\n\n")[1]
end_time = time.time()
total_time = end_time - start_time
print(o_answer)
print(f"Took a total time of {total_time} seconds")
"""

"""
# Define your prompt
prompt = "Explain the concept of reinforcement learning."

# Tokenize the input
inputs = tokenizer(prompt, return_tensors="pt").to(device)

start_time = time.time()
# Generate response
with torch.no_grad():
    output = model.generate(**inputs, temperature=0.6, max_new_tokens=1000, top_p=0.9)
end_time = time.time()
total_time = end_time - start_time
# Decode and print the response
response = tokenizer.decode(output[0], skip_special_tokens=True)
print("\n\n\n")
print(response)
print(f"Took a total time of {total_time} seconds")
print(f"Token generation rate of {output[0].shape[0]/total_time} tokens per second")
"""

