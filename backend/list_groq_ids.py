import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

def list_groq_ids():
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            models = [m['id'] for m in res.json()['data']]
            print("\n".join(sorted(models)))
        else:
            print(f"Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_groq_ids()
