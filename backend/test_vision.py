import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

def test_groq_vision():
    # Create a tiny 1x1 black pixel base64 for testing
    tiny_pixel_b64 = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Structure for Llama 3.2 Vision
    payload = {
        "model": "llama-3.2-11b-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{tiny_pixel_b64}"}}
                ]
            }
        ],
        "max_tokens": 100
    }
    
    print("Testing Groq Vision Request...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error Details: {response.text}")
        else:
            print(f"Success! Response: {response.json()['choices'][0]['message']['content']}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    test_groq_vision()
