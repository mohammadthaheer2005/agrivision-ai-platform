import requests
import json

payload = {
    "place": "Coimbatore",
    "state": "Tamil Nadu",
    "country": "India",
    "soil_type": "Alluvial",
    "season": "August",
    "language": "English"
}

try:
    res = requests.post("http://localhost:8002/api/geographic-intelligence", json=payload, timeout=30)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text[:200]}...")
except Exception as e:
    print(f"Error: {e}")
