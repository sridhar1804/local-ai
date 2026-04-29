import sys
sys.path.insert(0, "/home/ubuntu/ai/code")
from models.client import Phi3Client

c = Phi3Client()
# Test 1: no system prompt
r = c.generate("What is 2+2?", max_tokens=50, temperature=0.0)
print(f"Test 1 (no system): {r.completion!r}")

# Test 2: with system prompt
r2 = c.generate(
    "What is the capital of France?",
    system_message="You are a helpful assistant. Answer questions directly.",
    max_tokens=50,
    temperature=0.2
)
print(f"Test 2 (with system): {r2.completion!r}")
c.close()
