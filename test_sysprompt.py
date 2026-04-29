import sys
sys.path.insert(0, "/home/ubuntu/ai/code")
from models.client import Phi3Client

c = Phi3Client()
r = c.generate(
    "What is the capital of France?",
    system_message="You are a helpful, accurate, and concise AI assistant. Answer the user's question directly and clearly. If you are unsure, say so rather than guessing.",
    max_tokens=50,
    temperature=0.2
)
print(f"With system prompt: {r.completion!r}")

r2 = c.generate(
    "What is the capital of France?",
    max_tokens=50,
    temperature=0.2
)
print(f"Without system prompt: {r2.completion!r}")
c.close()
