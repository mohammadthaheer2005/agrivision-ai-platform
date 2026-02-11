import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

# Simulate the exact payload being sent
system_prompt = (
    "Role: Master Agri-Industrial Intelligence (ICAR Certified). Language: English. "
    "Expertise: You are a combined Senior Strategist, Geo-Tactical Advisor, and ICAR Pathologist. "
    "Instruction: Provide 100% accurate, localized, and deep Gemini-like reasoning for all agricultural queries. "
    "Context Awareness: ALWAYS use the provided location, soil, and season data to tailor your response. "
    "Deep Reasoning: If comparing crops or treatments, explain the EXACT climatic and industrial rationale. "
    "Mention ICAR standards and recommend EXACT Fertilizer brands (e.g., IFFCO, Tata, Coromandel)."
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "CONTEXT: Place: Coimbatore, State: Tamil Nadu, Soil: Alluvial, Season: August\nQUERY: why not sugarcane"}
]

payload = {"model": "llama-3.3-70b-versatile", "messages": messages, "temperature": 0.4}

print("Sending request to Groq...")
print(f"Payload size: {len(json.dumps(payload))} bytes")
print(f"Number of messages: {len(messages)}")

try:
    res = requests.post(url, json=payload, headers=headers, timeout=25)
    print(f"\nStatus Code: {res.status_code}")
    print(f"Response: {res.text}")
    
    if res.status_code == 200:
        print("\n✓ SUCCESS!")
        answer = res.json()['choices'][0]['message']['content']
        print(f"Answer: {answer[:200]}...")
    else:
        print("\n✗ ERROR!")
        print(f"Full error response: {res.text}")
except Exception as e:
    print(f"\n✗ EXCEPTION: {e}")
