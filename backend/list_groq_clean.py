import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

def list_groq_clean():
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            ids = [m['id'] for m in res.json()['data']]
            with open("groq_models_list.txt", "w") as f:
                f.write("\n".join(sorted(ids)))
            print("Model IDs written to groq_models_list.txt")
        else:
            print(f"Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_groq_clean()
