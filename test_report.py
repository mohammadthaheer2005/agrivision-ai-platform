import requests
import json

payload = {
    "data": {"temperature": 28.5, "ph": 6.5, "nitrogen": 2.5, "place": "Coimbatore", "state": "Tamil Nadu", "country": "India", "soil_type": "Alluvial", "season": "August"},
    "recommendation": "OFFICIAL RESPONSE:\nBased on the OFFICIAL BIO-SCAN DIAGNOSIS, the recommended chemical treatment for managing anthracnose in watermelon fruit is a COPPER-BASED FUNGICIDE.\n\nRECOMMENDED CHEMICAL TREATMENT:\n1. Copper Oxychloride (COC): A widely used copper-based fungicide effective against anthracnose in watermelon.\n2. Copper Hydroxide (CH): Another copper-based fungicide that can be used to control anthracnose in watermelon.\n3. Copper Sulfate (CS): A copper-based fungicide that can be used to manage anthracnose in watermelon.\n\nTREATMENT GUIDELINES:\n1. Application Rate: 0.1-0.2% (w/w).\n2. Frequency: 7-10 days.",
    "language": "English",
    "history": [
        {"role": "user", "content": "what chemical i need to use"},
        {"role": "assistant", "content": "OFFICIAL RESPONSE: Use COPPER-BASED FUNGICIDE."}
    ],
    "market_snapshot": {"Rice": {"price": 340, "change": 2.5}, "Cotton": {"price": 1200, "change": -1.2}},
    "condition_name": "Watermelon Anthracnose"
}

try:
    res = requests.post("http://localhost:8002/api/generate-report", json=payload, timeout=10)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")
except Exception as e:
    print(f"Error: {e}")
