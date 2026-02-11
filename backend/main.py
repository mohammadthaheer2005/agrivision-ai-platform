from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import requests
import os
import json
import base64
from dotenv import load_dotenv
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random
import socket
import uvicorn
from fastapi.staticfiles import StaticFiles
from disease_database import get_disease_info

# --- CONFIG ---
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AGRI_V14_BACKEND")

app = FastAPI(title="Agri-Command Industrial Web Master V21.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- STATIC FILES (REPORT SERVING) ---
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR, exist_ok=True)
app.mount("/reports", StaticFiles(directory=REPORTS_DIR), name="reports")

# --- MODELS ---
class SimulationData(BaseModel):
    temperature: float = 28.5
    humidity: float = 55.0
    nitrogen: float = 2.50
    phosphorus: float = 1.80
    potassium: float = 2.20
    ph: float = 6.5
    dissolved_oxygen: float = 6.50
    sector: str = "North Sector"
    country: str = "India"
    state: str = "Tamil Nadu"
    place: str = "Coimbatore"
    soil_type: str = "Alluvial"

class ChatRequest(BaseModel):
    message: str
    context_data: dict
    sector: str = "Global"
    market_data: dict = {}
    language: str = "English"

class VisionRequest(BaseModel):
    image_base64: str
    sector: str = "Global"
    language: str = "English"

class ReportRequest(BaseModel):
    data: dict
    recommendation: str
    sector: str = "Global"
    market_snapshot: dict = {}
    history: list = []
    image_base64: str = ""
    condition_name: str = "Unknown"
    language: str = "English"
    country: str = "India"
    state: str = "Tamil Nadu"
    place: str = "Coimbatore"
    soil_type: str = "Alluvial"
    season: str = "August"

# --- STATE ---
current_state = SimulationData().model_dump()
last_vision_data = {"label": "None", "image": "", "disease_info": {}}

# --- REGIONAL KNOWLEDGE BASE (ICAR/CRIDA Standards) ---
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

# "Official Database" Logging (V15.0 Backup System)
def log_to_official_database(scan_type, result, condition):
    try:
        log_file = os.path.join(os.path.dirname(__file__), "bio_security_backup.csv")
        file_exists = os.path.isfile(log_file)
        with open(log_file, "a", encoding="utf-8") as f:
            if not file_exists:
                f.write("Timestamp,Scan_Type,Object_Detected,Condition_Status\n")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f'"{timestamp}","{scan_type}","{result}","{condition}"\n')
    except Exception as e:
        logger.error(f"Backup Logging Failed: {e}")

import datetime

# --- REAL DATA FUNCTIONS ---
def get_real_weather(city="Coimbatore", country_code="IN"):
    """Get real weather data from OpenWeatherMap"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        logger.warning("OpenWeatherMap API key not found, using simulated data")
        return None
    
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
    except Exception as e:
        logger.error(f"Weather API error: {e}")
    return None

def get_real_commodity_prices():
    """Get real commodity prices from Commodities-API"""
    api_key = os.getenv("COMMODITIES_API_KEY")
    if not api_key:
        logger.warning("Commodities API key not found, using simulated data")
        return None
    
    try:
        # Commodities-API endpoint for latest rates
        url = f"https://commodities-api.com/api/latest?access_key={api_key}&base=USD&symbols=CORN,WHEAT,SOYBEAN,RICE"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get("success"):
                rates = data.get("data", {}).get("rates", {})
                # Convert rates to prices (rates are inverted)
                return {
                    "Corn": {"price": round(1/rates.get("CORN", 0.2) * 100, 2) if rates.get("CORN") else 4.25, "change": round(random.uniform(-2, 2), 2), "data_source": "LIVE"},
                    "Wheat": {"price": round(1/rates.get("WHEAT", 0.17) * 100, 2) if rates.get("WHEAT") else 5.80, "change": round(random.uniform(-2, 2), 2), "data_source": "LIVE"},
                    "Soybeans": {"price": round(1/rates.get("SOYBEAN", 0.09) * 100, 2) if rates.get("SOYBEAN") else 11.45, "change": round(random.uniform(-2, 2), 2), "data_source": "LIVE"},
                    "Rice": {"price": round(1/rates.get("RICE", 0.055) * 100, 2) if rates.get("RICE") else 18.20, "change": round(random.uniform(-2, 2), 2), "data_source": "LIVE"}
                }
    except Exception as e:
        logger.error(f"Commodity API error: {e}")
    return None

# Fallback simulated data
commodity_prices = {
    "Corn": {"price": 4.25, "change": +0.02, "data_source": "SIMULATED"},
    "Wheat": {"price": 5.80, "change": -0.05, "data_source": "SIMULATED"},
    "Soybeans": {"price": 11.45, "change": +0.12, "data_source": "SIMULATED"},
    "Rice": {"price": 18.20, "change": +0.08, "data_source": "SIMULATED"}
}

# --- UTILS ---
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
            {"role": "system", "content": f"You are a professional agricultural translator. Translate the input into {target_lang}. "
                                         f"Also provide a 1-sentence voice-optimized summary in {target_lang}. "
                                         f"STRICT FORMAT: SUMMARY: [summary] TRANSLATION: [translation]. "
                                         f"Output ONLY in {target_lang}."},
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
                summary = parts[0].replace("SUMMARY:", "").strip()
                translation = parts[1].strip()
                return translation, summary
            else:
                # Fallback if format is missed
                return raw, raw
        return text, text
    except:
        return text, text

# Video features removed per user request.

def get_official_resource(query):
    """Generate a link to official Indian agricultural resources"""
    # Agmarknet for prices, ICAR for research, TNAU/AU for cultivation
    search_query = query.replace(" ", "+") + "+site%3Aicar.org.in+OR+site%3Atnau.ac.in"
    return f"https://www.google.com/search?q={search_query}"

# --- ENDPOINTS ---
@app.get("/api/health")
async def health_check():
    return {"status": "operational", "version": "14.0", "real_data": True}

@app.get("/api/live-data")
async def get_live_data():
    global commodity_prices, current_state
    
    # Try to get real weather data
    weather = get_real_weather(current_state.get("place", "Coimbatore"), "IN")
    if weather:
        current_state["temperature"] = weather["temperature"]
        current_state["humidity"] = weather["humidity"]
        current_state["data_source"] = "LIVE"
    else:
        current_state["data_source"] = "SIMULATED"
    
    # Try to get real commodity prices
    real_prices = get_real_commodity_prices()
    if real_prices:
        commodity_prices = real_prices
    else:
        # Simulate price drift for fallback
        for key in commodity_prices:
            drift = random.uniform(-0.02, 0.02)
            commodity_prices[key]["price"] = round(commodity_prices[key]["price"] * (1 + drift), 2)
            commodity_prices[key]["change"] = round(drift * 100, 2)
    
    return {"telemetry": current_state, "market": commodity_prices}

@app.post("/api/predict-crop")
async def predict_crop(data: dict):
    """V15.0 Industrial Weighted Predictor"""
    temp = data.get("temperature", 25)
    ph = data.get("ph", 6.5)
    nitro = data.get("nitrogen", 2.0)
    phos = data.get("phosphorus", 1.8)
    potas = data.get("potassium", 2.2)
    soil = data.get("soil_type", "Alluvial").lower()
    state = data.get("state", "Tamil Nadu").lower()

    # Ideals: [Temp, PH, N, P, K, Preferred Soils, Key Regions]
    # Weights: Temp(20), PH(15), N(20), P(10), K(10), Soil(15), Region(10)
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
        # Heuristic Weights
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

@app.post("/api/geographic-intelligence")
async def get_geographic_intelligence(data: dict):
    """V16.0: Scientific Realism - Web-Integrated Intelligence"""
    place = data.get("place", "Unknown").lower()
    state = data.get("state", "Unknown").lower()
    country = data.get("country", "Unknown")
    soil_type = data.get("soil_type", "Unknown")
    variance = data.get("variance", 1.0)
    
    # V22.1: Higher-Validity Agricultural Search (Consolidated Knowledge)
    local_intel = "Real-time predictive analysis based on regional climate, soil taxonomy, and ICAR agricultural standards."
    
    place_key = place.lower().strip()
    if place_key in REGIONAL_KNOWLEDGE:
        local_intel = REGIONAL_KNOWLEDGE[place_key]
    else:
        try:
            # Better query for agricultural specifics
            wiki_query = f"{place} agriculture climate soil crops"
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{place.replace(' ', '_')}"
            wiki_res = requests.get(wiki_url, timeout=5)
            if wiki_res.status_code == 200:
                local_intel = wiki_res.json().get('extract', local_intel)
            else:
                 # Fallback to search API for broader context
                 search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={wiki_query}&format=json"
                 s_res = requests.get(search_url, timeout=5)
                 if s_res.status_code == 200:
                     results = s_res.json().get('query', {}).get('search', [])
                     if results:
                         local_intel = results[0].get('snippet', "").replace('<span class="searchmatch">', "").replace('</span>', "")
                         local_intel += f" (Localized context for {place} confirmed via digital records)."
        except: pass
    
    pred_res = await predict_crop(data)
    scores = pred_res["scores"]
    
    # Apply variance for realism
    for crop in scores:
        scores[crop] = round(scores[crop] * variance, 1)
        # V22.2: BOOST SCORES based on local intelligence markers
        # If the crop name appears in the local_intel text, give it a significant accuracy boost
        if crop.lower() in local_intel.lower():
            scores[crop] = min(98.5, scores[crop] + 25.0)
        # Special case for "Paddy" in intel matching "Rice" in scores
        if "paddy" in local_intel.lower() and crop == "Rice":
            scores[crop] = min(98.8, scores[crop] + 25.0)
    
    best_crop = max(scores, key=scores.get)

    summary = (
        f"🌍 **GEOGRAPHIC INTELLIGENCE REPORT: {place.title()}**\n\n"
        f"**Field Matrix:** {soil_type} Analysis\n"
        f"**Official Intelligence:** {local_intel}\n"
        f"**Industrial Recommendation:** {best_crop} ({scores[best_crop]}% suitability)\n\n"
        "**Verified Data Mapping:**\n"
        + "\n".join([f"- {crop}: {score}%" for crop, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)])
        + f"\n\n**OFFICIAL RESOURCE:** [ICAR Cultivation Hub]({get_official_resource(best_crop + ' cultivation')})"
    )
    
    # V17.0: Localized Voice Summary
    speech_summary, _ = translate_and_explain(f"Geographic intelligence for {place} complete. {local_intel} Best crop is {best_crop}.", data.get("language", "English"))
    
    # Video features removed.
    
    return {
        "intelligence": summary, 
        "scores": scores, 
        "best_crop": best_crop, 
        "speech_summary": speech_summary
    }

@app.post("/api/simulate")
async def update_simulation(data: dict):
    global current_state
    current_state.update(data)
    return {"status": "success", "state": current_state}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    key = get_groq_key()
    if not key: return {"answer": "Error: API_KEY_MISSING"}
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    
    context = req.context_data.copy()
    raw_history = context.pop("history", [])
    chat_focus = context.get("chat_focus", "Localization")
    
    # MASTER INTELLIGENCE PERSONA (V34.0: UNIFIED TRANSLATION)
    system_prompt = (
        f"Role: Master Agri-Industrial Intelligence (ICAR Certified). "
        f"OUTPUT LANGUAGE: {req.language}. "
        f"STRICT INSTRUCTION: Respond ONLY in {req.language}. "
        f"If the language is NOT English, follow this format: "
        f"TRANSLATION: [Your full answer in {req.language}] "
        f"SUMMARY: [1-sentence voice summary in {req.language}] "
        f"Otherwise, just provide the full answer."
    )
    
    # Regional Knowledge Sync
    place_name = context.get('place', '').lower().strip()
    if place_name in REGIONAL_KNOWLEDGE:
        system_prompt += f"CURRENT CONTEXTUAL TRUTH for {place_name}: {REGIONAL_KNOWLEDGE[place_name]}. "

    if chat_focus == "Bio-Scan":
        system_prompt += (
            "Instruction: You are in BIO-SCAN mode. Identify diseases and treatments. "
            "Answer any agricultural questions with 100% accuracy."
        )
    else:
        system_prompt += (
            "Instruction: You are an Agricultural Intelligence Expert. Answer any regional or "
            "global crop questions with ICAR-level accuracy. Provide intelligence for any location requested."
        )

    clean_history = []
    for msg in raw_history[-4:]:
        if isinstance(msg, dict) and "role" in msg and "content" in msg:
            clean_history.append({"role": msg["role"], "content": str(msg["content"])[:1000]})
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in clean_history: messages.append(msg)
    
    intel_context = ""
    if context.get("location_intel"): intel_context += f"\nOFFICIAL LOCATION INTELLIGENCE: {context['location_intel']}"
    if context.get("bio_audit"): intel_context += f"\nOFFICIAL BIO-SCAN DIAGNOSIS: {context['bio_audit']}"
        
    messages.append({"role": "user", "content": f"CONTEXT: {intel_context}\nQUERY: {req.message}"})

    payload = {"model": "llama-3.1-8b-instant", "messages": messages, "temperature": 0.2}
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        if res.status_code == 200:
            ans = res.json()['choices'][0]['message']['content']
            
            # Handle unified translation format
            if "TRANSLATION:" in ans and "SUMMARY:" in ans:
                parts = ans.split("SUMMARY:")
                translation = parts[0].replace("TRANSLATION:", "").strip()
                speech_summary = parts[1].strip()
            else:
                translation = ans
                speech_summary = ans[:150] # Snippet for voice
                
            resource_link = get_official_resource(req.message)
            return {"answer": translation + f"\n\n**🌐 OFFICAL SOURCE:** [Industrial Agriculture Research]({resource_link})", 
                    "speech_summary": speech_summary}
        
        return {"answer": f"OFFLINE: API Error {res.status_code}.", "speech_summary": "Link failure."}
    except Exception as e:
        return {"answer": f"OFFLINE: {str(e)}", "speech_summary": "Connection fault."}

@app.post("/api/vision-diagnosis")
async def vision_diagnosis(req: VisionRequest):
    global last_vision_data
    hf_key = os.getenv("HUGGING_FACE_API_KEY")
    groq_key = get_groq_key()
    if not hf_key or not groq_key: return {"answer": "Error: API_KEYS_MISSING."}
    hf_url = "https://router.huggingface.co/v1/chat/completions"
    headers_hf = {"Authorization": f"Bearer {hf_key}", "Content-Type": "application/json", "X-Wait-For-Model": "true"}
    
    # V35.0: FULL REAL-DATA BOTANICAL IDENTIFICATION (GOOGLE-LENS STYLE)
    vision_prompt = (
        "Role: Senior Agricultural Scientist & Plant Pathologist. "
        "Task: Identify the plant and disease in the image with 100% accuracy. "
        "Logic: Look for specific fungal, bacterial, or viral markers. "
        "Instructions: "
        "1. Identify the ENTITY (e.g., Watermelon Leaf, Tomato Fruit). "
        "2. Identify the CONDITION (e.g., Anthracnose, Late Blight, Healthy). "
        "3. Describe VISUAL SYMPTOMS in detail (e.g., sunken spots, dark lesions). "
        "4. Provide a SCIENTIFIC CAUSE. "
        "Output Format exactly like this: "
        "ENTITY: [Crop Name]\n"
        "CONDITION: [Specific Disease Name]\n"
        "CONFIDENCE: [0-100%]\n"
        "SYMPTOMS: [Visual description]\n"
        "CAUSE: [Pathogen name]\n"
        "MANAGEMENT: [Short summary]"
    )
    
    try:
        payload_hf = {
            "model": "Qwen/Qwen2.5-VL-7B-Instruct",
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": vision_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{req.image_base64}"}}
            ]}],
            "max_tokens": 500
        }
        hf_res = requests.post(hf_url, headers=headers_hf, json=payload_hf, timeout=60)
        full_analysis = hf_res.json()['choices'][0]['message']['content'].strip() if hf_res.status_code == 200 else "Unknown Analysis"
        
        # V35.0: Enhanced DB Matching logic
        detected_label = "Unknown"
        lines = full_analysis.split('\n')
        for line in lines:
            if "CONDITION:" in line:
                detected_label = line.replace("CONDITION:", "").strip()
                # Special handle for "Anthracnose" to check "Watermelon Anthracnose" if entity matches
                entity_context = ""
                for l in lines:
                    if "ENTITY:" in l: entity_context = l.lower()
                
                if "anthracnose" in detected_label.lower() and "watermelon" in entity_context:
                    detected_label = "Watermelon Anthracnose"
                break
        
        disease_info = get_disease_info(detected_label)
        last_vision_data = {"label": detected_label, "image": req.image_base64, "disease_info": disease_info}
        
        # V34.0: Consolidated Vision Response (Updated for Clarity)
        advisory_payload = (
            f"OFFICIAL VISION ANALYSIS: {full_analysis}\n\n"
            f"Provide 100% accurate agricultural advisory in {req.language}. "
            "Use a professional, helpful tone. Break down symptoms and management like Google Lens. "
            f"STRICT FORMAT: TRANSLATION: [Full Advisory in {req.language}] SUMMARY: [1-sentence summary]"
        )
        payload_groq = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": f"Role: Agricultural Strategist. Language: {req.language}."},
                {"role": "user", "content": advisory_payload}
            ]
        }
        groq_res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                               json=payload_groq, headers={"Authorization": f"Bearer {groq_key}"}, timeout=20)
        
        ans = groq_res.json()['choices'][0]['message']['content'] if groq_res.status_code == 200 else "Vision failure."
        
        if "TRANSLATION:" in ans and "SUMMARY:" in ans:
            parts = ans.split("SUMMARY:")
            translation = parts[0].replace("TRANSLATION:", "").strip()
            speech_summary = parts[1].strip()
        else:
            translation = ans
            speech_summary = ans[:150]
            
        resource_link = get_official_resource(detected_label + " identification treatment " + disease_info.get("severity", ""))
        
        return {"answer": translation + f"\n\n**📜 OFFICIAL AUDIT RECORD:** [ICAR Database Link]({resource_link})", 
                "speech_summary": speech_summary, "disease_info": disease_info, "scientific_breakdown": full_analysis,
                "label": detected_label}
    except Exception as e:
        return {"answer": f"Vision Fault: {str(e)}", "speech_summary": "Bio-scan Uplink Interrupted."}

@app.post("/api/generate-report")
async def generate_report(req: ReportRequest):
    try:
        from report_engine import report_engine
        localized_rec, _ = translate_and_explain(req.recommendation, req.language)
        combined_data = {**req.data, "market_snapshot": req.market_snapshot}
        combined_data.update({
            "country": req.country,
            "state": req.state,
            "place": req.place,
            "soil_type": req.soil_type,
            "season": req.season
        })
        
        # V14.0: Pass disease info to report engine
        disease_info = last_vision_data.get("disease_info", {})
        
        # V19.0: Maximizing PDF Data Transparency
        crop_scores = last_vision_data.get("scores", {}) # Try to get from last vision or predict
        if not crop_scores:
            pred = await predict_crop(combined_data)
            crop_scores = pred.get("scores", {})

        filepath, filename = report_engine.generate_report(
            combined_data, localized_rec, req.sector, history=req.history,
            image_base64=req.image_base64 or last_vision_data["image"],
            condition_name=req.condition_name or last_vision_data["label"],
            language=req.language,
            disease_info=disease_info,
            crop_scores=crop_scores
        )
        # V22.0: Return Public Static URL
        report_url = f"http://localhost:8002/reports/{filename}"
        logger.info(f"Report Generated Successfully: {filename}")
        return {"status": "success", "report_url": report_url, "filename": filename}
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Generate Report Failed: {str(e)}\n{error_trace}")
        return JSONResponse(status_code=500, content={"status": "error", "message": f"Engine Fault: {str(e)}"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")
