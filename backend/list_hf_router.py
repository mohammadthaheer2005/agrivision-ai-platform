import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
hf_key = os.getenv("HUGGING_FACE_API_KEY")

def list_hf_router_models():
    url = "https://router.huggingface.co/v1/models"
    headers = {"Authorization": f"Bearer {hf_key}"}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            models = res.json().get("data", [])
            ids = [m['id'] for m in models]
            with open("hf_router_models.txt", "w") as f:
                f.write("\n".join(sorted(ids)))
            print(f"Written {len(ids)} models to hf_router_models.txt")
        else:
            print(f"Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_hf_router_models()
