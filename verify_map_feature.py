import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

try:
    from backend import logic
    print("✓ Backend logic imported successfully.")
except ImportError as e:
    print(f"✗ Failed to import logic: {e}")
    sys.exit(1)

def test_geocoding():
    print("\n--- Testing Reverse Geocoding ---")
    # Coordinates for Buchireddypalem, Nellore
    lat, lon = 14.5367, 79.8821
    print(f"Coordinates: {lat}, {lon}")
    
    res = logic.reverse_geocode(lat, lon)
    if res:
        print(f"✓ Geocoding successful: {res}")
    else:
        print("✗ Geocoding failed.")

def test_intelligence_logic():
    print("\n--- Testing Geographic Intelligence AI ---")
    data = {
        "place": "Buchireddypalem",
        "state": "Andhra Pradesh",
        "country": "India",
        "lat": 14.5367,
        "lon": 79.8821,
        "language": "English"
    }
    
    print(f"Sending request for: {data['place']}...")
    res = logic.get_geographic_intelligence_logic(data)
    
    if "intelligence" in res:
        print("✓ AI Intelligence Report generated.")
        print("-" * 30)
        print(res["intelligence"][:500] + "...")
        print("-" * 30)
    else:
        print("✗ Intelligence generation failed.")

def test_forward_geocoding():
    print("\n--- Testing Forward Geocoding (Search) ---")
    query = "Buchireddypalem, Nellore, Andhra Pradesh"
    print(f"Query: {query}")
    res = logic.forward_geocode(query)
    if res:
        print(f"✓ Forward geocoding successful: {res}")
    else:
        print("✗ Forward geocoding failed.")

if __name__ == "__main__":
    # Note: This requires geopy and requests to be installed in the environment
    # and a valid GROQ_API_KEY in the .env file.
    test_geocoding()
    test_forward_geocoding()
    test_intelligence_logic()
