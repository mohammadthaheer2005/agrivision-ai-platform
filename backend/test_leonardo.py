import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("LEONARDO_API_KEY")

def test_leonardo():
    print(f"Testing Leonardo API Key: {api_key[:5]}...{api_key[-5:]}")
    url = "https://cloud.leonardo.ai/api/rest/v1/me"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("✅ Leonardo API Key is VALID.")
            print(f"User Info: {response.json()}")
        else:
            print(f"❌ Leonardo API Key is INVALID. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error connecting to Leonardo: {e}")

if __name__ == "__main__":
    test_leonardo()
