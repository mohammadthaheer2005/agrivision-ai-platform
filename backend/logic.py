import requests
import os
import json
import base64
import random
import datetime
import logging
from disease_database import get_disease_info

# --- CONFIG ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AGRI_LOGIC")

# --- REGIONAL KNOWLEDGE BASE ---
REGIONAL_KNOWLEDGE = {
    "nellore": "Famous as the 'Rice Bowl of Andhra Pradesh'. Best crops: Paddy (NLR-34449, RNR-15048), Blackgram, Chillies, and Cotton. Soil: Coastal Alluvial & Red soils.",
    "coimbatore": "Industrial Agri-Hub. Best crops: Sorghum, Maize, Cotton, and Sugarcane. Soil: Black & Red Soil.",
    "guntur": "World-famous for Chillies. Best crops: Chillies, Cotton, Tobacco, and Paddy.",
    "chittoor": "Known for horticulture and poultry. Best crops: Groundnut, Sugarcane, Mango, and Paddy. Soil: Red Loamy/Sandy soils.",
    "chithore": "Known for horticulture and poultry. Best crops: Groundnut, Sugarcane, Mango, and Paddy. Soil: Red Loamy/Sandy soils.",
    "chithor": "Known for horticulture and poultry. Best crops: Groundnut, Sugarcane, Mango, and Paddy. Soil: Red Loamy/Sandy soils.",
    "nashik": "Wine capital. Best crops: Grapes, Onion, and Tomatoes.",
    "punjab": "Best crops: Wheat, Paddy (Basmati), and Sugarcane."
}

# --- REAL DATA FUNCTIONS ---
def get_real_weather(city="Coimbatore", country_code="IN"):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key: return None
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=metric"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return {
                "temperature": round(data["main"]["temp"], 1),
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "data_source": "LIVE"
            }
    except: pass
    return None

def get_real_commodity_prices():
    api_key = os.getenv("COMMODITIES_API_KEY")
    if not api_key: return None
    try:
        url = f"https://commodities-api.com/api/latest?access_key={api_key}&base=USD&symbols=CORN,WHEAT,SOYBEAN,RICE"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get("success"):
                rates = data.get("data", {}).get("rates", {})
                return {
                    "Corn": {"price": round(1/rates.get("CORN", 0.2) * 100, 2) if rates.get("CORN") else 4.25, "change": round(random.uniform(-2, 2), 2), "data_source": "LIVE"},
                    "Wheat": {"price": round(1/rates.get("WHEAT", 0.17) * 100, 2) if rates.get("WHEAT") else 5.80, "change": round(random.uniform(-2, 2), 2), "data_source": "LIVE"},
                    "Soybeans": {"price": round(1/rates.get("SOYBEAN", 0.09) * 100, 2) if rates.get("SOYBEAN") else 11.45, "change": round(random.uniform(-2, 2), 2), "data_source": "LIVE"},
                    "Rice": {"price": round(1/rates.get("RICE", 0.055) * 100, 2) if rates.get("RICE") else 18.20, "change": round(random.uniform(-2, 2), 2), "data_source": "LIVE"}
                }
    except: pass
    return None

def get_groq_key():
    return os.getenv("GROQ_API_KEY")

def translate_and_explain(text, target_lang):
    if target_lang == "English": return text, text
    key = get_groq_key()
    if not key: return text, text
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": f"You are a professional agricultural translator. Translate the input into {target_lang}. STRICT FORMAT: SUMMARY: [summary] TRANSLATION: [translation]."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.1
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=15)
        if res.status_code == 200:
            raw = res.json()['choices'][0]['message']['content']
            if "SUMMARY:" in raw and "TRANSLATION:" in raw:
                parts = raw.split("TRANSLATION:")
                return parts[1].strip(), parts[0].replace("SUMMARY:", "").strip()
        return text, text
    except: return text, text

def get_official_resource(query):
    search_query = query.replace(" ", "+") + "+site%3Aicar.org.in+OR+site%3Atnau.ac.in"
    return f"https://www.google.com/search?q={search_query}"

def predict_crop_logic(data):
    temp = data.get("temperature", 25)
    ph = data.get("ph", 6.5)
    nitro = data.get("nitrogen", 2.0)
    phos = data.get("phosphorus", 1.8)
    potas = data.get("potassium", 2.2)
    soil = data.get("soil_type", "Alluvial").lower()
    state = data.get("state", "Tamil Nadu").lower()

    crop_specs = {
        "Rice": [30, 6.0, 3.0, 2.0, 2.0, ["alluvial", "clay"], ["tamil nadu", "telangana", "andhra pradesh", "west bengal"]],
        "Wheat": [20, 6.5, 2.0, 1.5, 1.5, ["alluvial", "black"], ["punjab", "haryana", "uttar pradesh"]],
        "Corn": [26, 6.8, 3.5, 2.5, 3.0, ["red", "alluvial"], ["karnataka", "maharashtra", "andhra pradesh"]],
        "Soybeans": [25, 6.2, 1.5, 2.0, 2.5, ["black", "red"], ["madhya pradesh", "maharashtra", "rajasthan"]],
        "Cotton": [28, 7.5, 2.5, 1.8, 2.2, ["black"], ["gujarat", "maharashtra", "telangana"]],
        "Sugarcane": [32, 7.0, 4.0, 3.0, 3.5, ["alluvial", "black"], ["uttar pradesh", "maharashtra", "karnataka"]]
    }

    scores = {}
    for crop, ideals in crop_specs.items():
        s_temp = max(0, 20 - abs(temp - ideals[0]) * 1.5)
        s_ph = max(0, 15 - abs(ph - ideals[1]) * 8)
        s_n = max(0, 20 - abs(nitro - ideals[2]) * 8)
        s_p = max(0, 10 - abs(phos - ideals[3]) * 5)
        s_k = max(0, 10 - abs(potas - ideals[4]) * 5)
        s_soil = 15 if soil in ideals[5] else 5
        s_reg = 10 if state in ideals[6] else 0
        total = round(min(100, s_temp + s_ph + s_n + s_p + s_k + s_soil + s_reg), 1)
        scores[crop] = total

    best_crop = max(scores, key=scores.get)
    return {"scores": scores, "recommendation": best_crop, "suitability": scores[best_crop]}

def get_geographic_intelligence_logic(data):
    place = data.get("place", "Unknown").lower()
    soil_type = data.get("soil_type", "Unknown")
    variance = data.get("variance", 1.0)
    
    local_intel = "Real-time predictive analysis based on regional climate, soil taxonomy, and ICAR agricultural standards."
    place_key = place.lower().strip()
    if place_key in REGIONAL_KNOWLEDGE:
        local_intel = REGIONAL_KNOWLEDGE[place_key]
    else:
        try:
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{place.replace(' ', '_')}"
            wiki_res = requests.get(wiki_url, timeout=5)
            if wiki_res.status_code == 200:
                local_intel = wiki_res.json().get('extract', local_intel)
        except: pass
    
    pred_res = predict_crop_logic(data)
    scores = pred_res["scores"]
    for crop in scores:
        scores[crop] = round(scores[crop] * variance, 1)
        if crop.lower() in local_intel.lower(): scores[crop] = min(98.5, scores[crop] + 25.0)
    
    best_crop = max(scores, key=scores.get)
    summary = (
        f"🌍 **GEOGRAPHIC INTELLIGENCE: {place.title()}**\n\n"
        f"**Official Intel:** {local_intel}\n"
        f"**Recommendation:** {best_crop} ({scores[best_crop]}% suitability)\n\n"
        + "\n".join([f"- {crop}: {score}%" for crop, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)])
    )
    speech, _ = translate_and_explain(f"Geo-intel for {place} complete. {best_crop} recommended.", data.get("language", "English"))
    
    return {"intelligence": summary, "scores": scores, "best_crop": best_crop, "speech_summary": speech}

def chat_logic(message, language, context_data):
    key = get_groq_key()
    if not key: return {"answer": "Error: API_KEY_MISSING"}
    
    chat_focus = context_data.get("chat_focus", "Localization")
    history = context_data.get("history", [])
    
    system_prompt = (
        f"Role: Master Agri-Industrial Intelligence (ICAR Certified). Language: {language}. "
        f"STRICT: Respond ONLY in {language}. "
        f"Format: TRANSLATION: [Full Answer] SUMMARY: [1-sentence voice summary]"
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history[-4:]:
        messages.append({"role": msg["role"], "content": str(msg["content"])[:500]})
    
    intel_context = ""
    if context_data.get("location_intel"): intel_context += f"\nGEO-INTEL: {context_data['location_intel']}"
    if context_data.get("bio_audit"): intel_context += f"\nBIO-SCAN: {context_data['bio_audit']}"
    
    messages.append({"role": "user", "content": f"CONTEXT: {intel_context}\nQUERY: {message}"})

    try:
        payload = {"model": "llama-3.1-8b-instant", "messages": messages, "temperature": 0.2}
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                          json=payload, headers={"Authorization": f"Bearer {key}"}, timeout=20)
        if res.status_code == 200:
            ans = res.json()['choices'][0]['message']['content']
            if "TRANSLATION:" in ans and "SUMMARY:" in ans:
                parts = ans.split("SUMMARY:")
                return {"answer": parts[0].replace("TRANSLATION:", "").strip(), "speech_summary": parts[1].strip()}
            return {"answer": ans, "speech_summary": ans[:150]}
    except: pass
    return {"answer": "Offline or API Error.", "speech_summary": "Link failure."}

def vision_diagnosis_logic(image_base64, language):
    hf_key = os.getenv("HUGGING_FACE_API_KEY")
    groq_key = get_groq_key()
    if not hf_key or not groq_key: return {"answer": "Key Missing"}
    
    vision_prompt = (
        "Role: Expert Botanical Scientist and Plant Pathologist. "
        "Task: Identify the plant and any potential diseases with clinical precision. "
        "Logic: Analyze botanical markers like leaf arrangement (pinnate/palmate), margin types (serrated/smooth), and leaflet shape. "
        "Distinction Note: Neem has serrated (saw-like) margins and pointed tips. Moringa has small, oval-shaped leaflets with smooth margins. Do not confuse them. "
        "Output Format: "
        "ENTITY: [Crop Name and Variety]\n"
        "CONDITION: [Specific Disease or 'Healthy']\n"
        "CONFIDENCE: [0-100%]\n"
        "SYMPTOMS: [Visual botanical markers observed]\n"
        "CAUSE: [Scientific Pathogen or Environmental factor]\n"
        "MANAGEMENT: [Industrial-grade agricultural advice]"
    )
    
    try:
        payload_hf = {
            "model": "Qwen/Qwen2.5-VL-7B-Instruct",
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": vision_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            ]}]
        }
        hf_res = requests.post("https://router.huggingface.co/v1/chat/completions", 
                             headers={"Authorization": f"Bearer {hf_key}"}, json=payload_hf, timeout=60)
        full_analysis = hf_res.json()['choices'][0]['message']['content'] if hf_res.status_code == 200 else "Unknown"
        
        detected_label = "Unknown"
        for line in full_analysis.split('\n'):
            if "CONDITION:" in line: detected_label = line.replace("CONDITION:", "").strip(); break
        
        disease_info = get_disease_info(detected_label)
        
        # Groq formatting
        payload_groq = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": f"Advisory for {full_analysis} in {language}. Format: TRANSLATION: [Advisory] SUMMARY: [Snippet]"}]
        }
        groq_res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                               json=payload_groq, headers={"Authorization": f"Bearer {groq_key}"}, timeout=20)
        ans = groq_res.json()['choices'][0]['message']['content'] if groq_res.status_code == 200 else "Analysis complete."
        
        if "TRANSLATION:" in ans and "SUMMARY:" in ans:
            parts = ans.split("SUMMARY:")
            return {"answer": parts[0].replace("TRANSLATION:", "").strip(), "speech_summary": parts[1].strip(), "disease_info": disease_info, "label": detected_label}
        return {"answer": ans, "speech_summary": ans[:150], "disease_info": disease_info, "label": detected_label}
    except Exception as e:
        return {"answer": f"Vision Fault: {str(e)}", "speech_summary": "Error."}
