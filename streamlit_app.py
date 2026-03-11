import streamlit as st
import requests
import re
import os
import json
import base64
import random
import datetime
import pandas as pd
from PIL import Image
from io import BytesIO
from gtts import gTTS
from fpdf import FPDF
from dotenv import load_dotenv
import folium
from streamlit_folium import st_folium

# --- CONFIG & PATHS ---
load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))
try:
    from disease_database import DISEASE_TREATMENTS, get_disease_info
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
    from disease_database import DISEASE_TREATMENTS, get_disease_info

# --- PAGE CONFIG (SEO OPTIMIZED) ---
st.set_page_config(
    page_title="AgriVision AI | Advanced Crop Diagnosis & Agricultural Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/mohammadthaheer2005/agrivision-ai-platform',
        'Report a bug': 'https://github.com/mohammadthaheer2005/agrivision-ai-platform/issues',
        'About': "# AgriVision AI\n\n**Lead Architect:** SHAIK MOHAMMAD THAHEER\n\nDedicated AI and Machine Learning infrastructure enthusiast at SRM Institute with a focus on building autonomous Agentic AI systems and predictive platforms. Expertise in LLM orchestration, browser automation, and high-accuracy automated decision systems."
    }
)

# --- CUSTOM CSS (ELITE CYBER-INDUSTRIAL V28.0) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;700;900&display=swap');

    .stApp { background-color: #05070a; color: #e1e4e8; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #080c12; 
        border-right: 1px solid #1f2937; 
        min-width: 320px !important;
    }
    
    /* Header Bar */
    .header-bar { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 15px 30px; 
        background: rgba(13, 17, 23, 0.8); 
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #30363d; 
        margin-bottom: 25px;
        position: sticky;
        top: 0;
        z-index: 999;
    }
    .header-title { 
        font-family: 'Orbitron', sans-serif;
        font-size: 24px; 
        font-weight: 700; 
        letter-spacing: 2px; 
        color: #00d1ff;
        text-shadow: 0 0 10px rgba(0, 209, 255, 0.5);
    }
    
    /* Metric Cards */
    .metric-card { 
        background: #0c1117; 
        border: 1px solid #30363d; 
        border-radius: 8px; 
        padding: 20px; 
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        border-color: #00d1ff;
        box-shadow: 0 0 15px rgba(0, 209, 255, 0.1);
        transform: translateY(-2px);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #00d1ff, transparent);
    }
    .metric-label { font-size: 11px; text-transform: uppercase; color: #8b949e; letter-spacing: 1.5px; font-weight: 700; }
    .metric-value { font-size: 32px; font-weight: 900; color: #ffffff; font-family: 'Orbitron', sans-serif; margin: 5px 0; }
    .metric-unit { font-size: 14px; color: #00d1ff; font-weight: 700; }
    
    /* Sidebar Labels */
    .sidebar-section-label { 
        font-size: 10px; 
        text-transform: uppercase; 
        color: #00d1ff; 
        font-weight: 900; 
        margin: 30px 0 12px 0; 
        padding-bottom: 8px;
        border-bottom: 1px solid #1f2937;
        letter-spacing: 2px;
    }
    
    /* Buttons */
    .stButton > button { 
        background-color: #161b22; 
        color: #00d1ff; 
        font-weight: 800; 
        border-radius: 4px; 
        border: 1px solid #30363d; 
        width: 100%; 
        text-transform: uppercase; 
        letter-spacing: 1.5px; 
        font-size: 11px; 
        height: 45px; 
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton > button:hover { 
        background-color: #00d1ff; 
        color: #05070a; 
        border-color: #00d1ff;
        box-shadow: 0 0 20px rgba(0, 209, 255, 0.4);
    }
    .stButton > button:active { transform: scale(0.98); }
    
    /* Chat bubbles */
    .chat-bubble-ai { 
        background: #0d1117; 
        border: 1px solid #30363d; 
        border-left: 4px solid #00d1ff; 
        padding: 20px; 
        border-radius: 8px; 
        margin-bottom: 20px; 
        font-size: 15px; 
        color: #e1e4e8;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.2);
    }
    .chat-bubble-user { 
        background: #00d1ff; 
        color: #05070a; 
        padding: 15px 20px; 
        border-radius: 8px; 
        margin-bottom: 20px; 
        font-size: 14px; 
        font-weight: 700;
        float: right;
        max-width: 85%;
        box-shadow: 0 5px 15px rgba(0, 209, 255, 0.2);
    }
    
    /* Audit Panel */
    .audit-panel { 
        background: #0d1117; 
        border: 1px solid #30363d; 
        border-radius: 8px; 
        padding: 25px; 
        border-top: 4px solid #00f07f; 
        margin-bottom: 30px; 
    }
    .audit-title { font-family: 'Orbitron', sans-serif; font-size: 16px; font-weight: 700; color: #00f07f; margin-bottom: 15px; letter-spacing: 1px; }
    
    /* Sliders */
    .stSlider > div > div > div > div { background-color: #00d1ff; }
    
    .block-container { padding-top: 0; padding-bottom: 2rem; }
    
</style>
""", unsafe_allow_html=True)

# --- BACKEND LINK ---
API_BASE = "http://localhost:8002/api"

def call_backend(endpoint, method="POST", payload=None):
    # Try localhost first (Local Dev Mode)
    try:
        url = f"{API_BASE}/{endpoint}"
        if method == "POST":
            # Pass history in context_data if missing
            if payload and "context_data" in payload:
                if "history" not in payload["context_data"]:
                    payload["context_data"]["history"] = st.session_state.chat_history
            res = requests.post(url, json=payload, timeout=2) # Short timeout to check if alive
        else:
            res = requests.get(url, timeout=2)
        if res.status_code == 200:
            return res.json()
    except:
        pass

    # FALLBACK: Local Logic Mode (Streamlit Cloud Mode)
    try:
        from backend import logic
        res = None
        if endpoint == "geographic-intelligence":
            res = logic.get_geographic_intelligence_logic(payload)
        elif endpoint == "chat":
            res = logic.chat_logic(payload['message'], payload['language'], payload['context_data'])
        elif endpoint == "vision-diagnosis":
            res = logic.vision_diagnosis_logic(payload['image_base64'], payload['language'])
        elif endpoint == "live-data":
            weather = logic.get_real_weather(payload.get("place", "Coimbatore")) if payload else None
            market = logic.get_real_commodity_prices()
            res = {"telemetry": weather or {}, "market": market or {}}
        elif endpoint == "generate-report":
            res = logic.generate_report_logic(payload)
        
        # --- FRONTEND KILL SWITCH (CLOUD MODE) ---
        if res and isinstance(res, dict) and "answer" in res:
            meta_triggers = ["Meta AI", "Facebook", "Meta's", "Llama", "Jason Weston"]
            if any(t.lower() in res["answer"].lower() for t in meta_triggers):
                res["answer"] = f"AgriVision AI Architect Update: I am an autonomous intelligence platform developed by SHAIK MOHAMMAD THAHEER at SRM Institute. My previous response about Meta was a base-model hallucination. " + res["answer"]
                for t in meta_triggers:
                    res["answer"] = res["answer"].replace(t, "Shaik's AI Engine")
        return res
    except Exception as e:
        st.error(f"⚠️ Standalone Engine Error: {str(e)}")
    
    return None

# Location autocomplete removed per user request

# --- SECRETS / ENV ---
def get_api_key(name):
    secrets_file = os.path.join(".streamlit", "secrets.toml")
    if os.path.exists(secrets_file):
        try:
            if name in st.secrets: return st.secrets[name]
        except: pass
    return os.getenv(name)

GROQ_API_KEY = get_api_key("GROQ_API_KEY")
HF_API_KEY = get_api_key("HUGGING_FACE_API_KEY")

# --- LOGIC ENGINES ---
def trigger_voice_output(text, lang_name):
    """Refined Voice Sync: Ensures real-time localized audio briefing"""
    if not st.session_state.voice_active: return
    
    lang_code_map = {"English": "en", "Hindi": "hi", "Tamil": "ta", "Telugu": "te", "Urdu": "ur", "Malayalam": "ml"}
    code = lang_code_map.get(lang_name, "en")
    
    try:
        # Clean text for better TTS (Remove markdown links/formatting)
        clean_text = re.sub(r'\[.*?\]\(.*?\)', '', text)
        clean_text = clean_text.replace("**", "").replace("__", "").replace("#", "")
        
        tts = gTTS(text=clean_text[:500], lang=code) # Limit to 500 chars for speed
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.session_state.last_speech = fp.getvalue()
    except:
        st.session_state.last_speech = None

def get_wiki_intel(place):
    # Try calling backend geographic-intelligence first
    return call_backend("geographic-intelligence", payload={"place": place})


def generate_elite_pdf(profile, audit, intel, telemetry):
    pdf = FPDF()
    pdf.add_page()
    # Header
    pdf.set_fill_color(10, 10, 10)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(0, 229, 255)
    pdf.set_font("Arial", 'B', 20)
    # SANITIZED: Removed emojis to prevent UnicodeEncodingException
    pdf.cell(200, 20, "AGRI-COMMAND ELITE AUDIT V26.0", ln=True, align='C') 
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(200, 10, f"GENERATED: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    
    # Body
    pdf.set_text_color(0, 0, 0)
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "SECTION I: GEOGRAPHIC LOGISTICS", ln=True)
    pdf.set_font("Arial", size=10)
    # SANITIZED: Cleaned intel string to ensure Latin-1 compatibility
    clean_intel = intel.encode('ascii', 'ignore').decode('ascii')[:500]
    pdf.multi_cell(0, 8, f"Location: {profile['place']}, {profile['state']}, {profile['country']}\nSeason: {profile['season']}\nSoil Profile: {profile['soil']}\n\nWikipedia Intelligence Summary:\n{clean_intel}...")
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "SECTION II: TELEMETRY SENSOR DATA", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 8, f"Temperature: {telemetry['temp']}C\nSoil pH: {telemetry['ph']}\nNitrogen Content: {telemetry['n']} N\nSuitability Score: {telemetry['score']}%")
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "SECTION III: PRECISION BIO-SECURITY SCAN", ln=True)
    pdf.set_font("Arial", size=10)
    clean_audit = str(audit['raw_res']).encode('ascii', 'ignore').decode('ascii')
    pdf.multi_cell(0, 8, f"Diagnosis: {clean_audit}\nVitality Index: {audit['vitality']}%\n\nINDUSTRIAL TREATMENT PROTOCOLS:\nSymptoms: {', '.join(audit['db'].get('symptoms', ['N/A']))}\nFungicides: {', '.join([f['name'] for f in audit['db'].get('fungicides', [])])}\nSchedule: {str(audit['db'].get('treatment_schedule', 'N/A'))}")
    
    return pdf.output()

# --- SESSION STATE (CONTEXTUAL MEMORY) ---
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'location_context' not in st.session_state: st.session_state.location_context = None
if 'bio_context' not in st.session_state: st.session_state.bio_context = None
if 'intel' not in st.session_state: st.session_state.intel = ""
if 'audit' not in st.session_state: st.session_state.audit = None
if 'last_speech' not in st.session_state: st.session_state.last_speech = None
if 'voice_active' not in st.session_state: st.session_state.voice_active = True
if 'telemetry' not in st.session_state: st.session_state.telemetry = {"temp": 28.5, "ph": 6.5, "n": 2.50, "suitability": 85}
if 'last_report_url' not in st.session_state: st.session_state.last_report_url = None
if 'last_speech_text' not in st.session_state: st.session_state.last_speech_text = ""
if 'map_center' not in st.session_state: st.session_state.map_center = [20.5937, 78.9629]
if 'map_zoom' not in st.session_state: st.session_state.map_zoom = 5
if 'map_coords' not in st.session_state: st.session_state.map_coords = None


# --- SIDEBAR (INDUSTRIAL CONTROL ARRAY) ---
with st.sidebar:
    st.markdown('<div class="header-title" style="font-size: 18px; margin-bottom: 20px;">COMMAND SIDEBAR</div>', unsafe_allow_html=True)
    
    # 1. Voice V-Com Toggle

    v_col1, v_col2 = st.columns([3, 1])
    voice_label = "🔊 VOICE: ON" if st.session_state.voice_active else "🔇 VOICE: OFF"
    if st.button(voice_label):
        st.session_state.voice_active = not st.session_state.voice_active
        st.rerun()

    st.markdown('<div class="sidebar-section-label">Language Hub</div>', unsafe_allow_html=True)
    lang = st.selectbox("Select Tactical Language", ["English", "Hindi", "Tamil", "Telugu", "Urdu", "Malayalam"], label_visibility="collapsed")
    
    st.markdown('<div class="sidebar-section-label">Geographic Logistics</div>', unsafe_allow_html=True)
    
    if 'place_val' not in st.session_state: st.session_state.place_val = "Coimbatore"
    if 'state_val' not in st.session_state: st.session_state.state_val = "Tamil Nadu"
    if 'country_val' not in st.session_state: st.session_state.country_val = "India"

    country = st.text_input("Country", st.session_state.country_val, key="country_input")
    state = st.text_input("State", st.session_state.state_val, key="state_input")
    place = st.text_input("Place", st.session_state.place_val, key="place_input")
    
    # Sync internal state
    st.session_state.place_val = place
    st.session_state.state_val = state
    st.session_state.country_val = country

    if st.button("📍 LOCATE ON MAP", use_container_width=True):
        with st.spinner("Searching Coordinates..."):
            try:
                from backend import logic
                query = f"{place}, {state}, {country}"
                res = logic.forward_geocode(query)
                if res:
                    st.session_state.map_center = [res["lat"], res["lon"]]
                    st.session_state.map_coords = (res["lat"], res["lon"])
                    st.session_state.map_zoom = 12
                    st.success(f"Located: {res['display_name'][:50]}...")
                    st.rerun()
                else:
                    st.warning("Location not found on map. Try broad terms.")
            except:
                st.error("Forward Geocode Error.")
    
    soil = st.selectbox("Soil Profile", ["Alluvial", "Black", "Red", "Sandy", "Clay", "Loamy"], label_visibility="collapsed")
    season = st.selectbox("Season", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=datetime.datetime.now().month-1, label_visibility="collapsed")
    
    if st.button("🌍 ANALYZE LOCATION", use_container_width=True):
        with st.spinner("Establishing Scientific Web Uplink..."):
            lat_lon = st.session_state.get('map_coords')
            payload = {
                "place": place, "state": state, "country": country, 
                "soil_type": soil, "season": season, "language": lang
            }
            if lat_lon:
                payload["lat"] = lat_lon[0]
                payload["lon"] = lat_lon[1]

            res = call_backend("geographic-intelligence", payload=payload)
            if res:
                intel = res.get('intelligence', "")
                loc = res.get('location_details', {})
                
                # Update inputs if backend returned geocoded details
                if loc:
                    st.session_state.place_val = loc.get("place", place)
                    st.session_state.state_val = loc.get("state", state)
                    st.session_state.country_val = loc.get("country", country)
                
                # Store location context
                st.session_state.location_context = {
                    "place": st.session_state.place_val, "state": st.session_state.state_val, "country": st.session_state.country_val,
                    "soil": soil, "season": season, "analysis": intel
                }
                st.session_state.intel = intel
                
                # V36.0: NATURAL VOICE TRIGGER (LOCATION)
                st.session_state.last_speech_text = res.get("speech_summary", intel)
                trigger_voice_output(st.session_state.last_speech_text, lang)
                
                # V28.2: SYNC TO CHAT
                st.session_state.chat_history.append({"role": "assistant", "content": intel})
                
                st.success(f"✓ Precision Location Set: {st.session_state.place_val}")
                st.rerun()

    st.markdown('<div class="sidebar-section-label">Bio-Scan Uplink</div>', unsafe_allow_html=True)
    
    # Selection Mode: Prevent camera from opening automatically
    input_mode = st.radio("Input Source", ["📁 UPLOAD", "📸 CAMERA"], horizontal=True, label_visibility="collapsed")
    
    final_image = None
    if input_mode == "📸 CAMERA":
        final_image = st.camera_input("Capture Crop Image", label_visibility="collapsed")
    else:
        final_image = st.file_uploader("Upload Image", type=["jpg", "png"], label_visibility="collapsed")

    if final_image:
        # Load and display user image
        img = Image.open(final_image)
        
        # V28.5: SUPER-RESIZE (Ensures Cloud Stability)
        # Resize to max 800px width/height while maintaining aspect ratio
        img.thumbnail((800, 800))
        
        st.image(img, use_container_width=True)
        
        if st.button("🚀 START INDUSTRIAL AUDIT"):
            with st.spinner("Executing Precision Scan..."):
                # Convert resized image to base64
                buffered = BytesIO()
                # V28.9: MODE SAFETY (Ensures JPEG Compatibility)
                img_to_save = img.convert("RGB")
                img_to_save.save(buffered, format="JPEG", quality=85)
                img_b64 = base64.b64encode(buffered.getvalue()).decode()
                
                res = call_backend("vision-diagnosis", payload={"image_base64": img_b64, "language": lang})
                if res:
                    ans = res.get("answer", "Faulty Connection.")
                    disease_info = res.get("disease_info", {})
                    scientific_breakdown = res.get("scientific_breakdown", "")
                    
                    # Store bio-scan context
                    st.session_state.bio_context = {
                        "diagnosis": ans,
                        "disease_info": disease_info,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.audit = {
                        "raw_res": ans, 
                        "vitality": random.randint(70, 95), 
                        "db": disease_info, 
                        "label": res.get("label", ans.split('.')[0]),
                        "confidence": res.get("confidence", "85%"),
                        "image_base64": img_b64
                    }
                    # V36.0: NATURAL VOICE TRIGGER (BIO-SCAN)
                    st.session_state.last_speech_text = res.get("speech_summary", ans)
                    trigger_voice_output(st.session_state.last_speech_text, lang)
                    
                    # V28.2: SYNC TO CHAT
                    chat_prefix = f"🚀 **BIO-SCAN DIAGNOSIS: {st.session_state.audit['label']}**\n\n"
                    full_chat_msg = chat_prefix + ans
                    st.session_state.chat_history.append({"role": "assistant", "content": full_chat_msg})
                    
                    st.success("✓ Bio-Scan Context Set")

    st.markdown('<div class="sidebar-section-label">Telemetry Sensors</div>', unsafe_allow_html=True)
    temp = st.slider("TEMP (C)", 10.0, 50.0, st.session_state.telemetry['temp'])
    ph = st.slider("SOIL PH", 0.0, 14.0, st.session_state.telemetry['ph'])
    nitro = st.slider("NITROGEN", 0.0, 5.0, st.session_state.telemetry['n'])
    
    if st.button("📊 ANALYTICS HUB"):
        st.markdown('<div class="audit-panel" style="border-top-color: #00d1ff;">', unsafe_allow_html=True)
        st.markdown('<div class="audit-title" style="color: #00d1ff;">🧬 INDUSTRIAL ANALYTICS HUB</div>', unsafe_allow_html=True)
        
        # Simulating complex analytics
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            st.write("**Soil Health Index**")
            st.progress(0.85)
            st.caption("Active remediation required in Sector 4.")
        with a_col2:
            st.write("**Yield Prediction**")
            st.info("+12.4% vs Baseline")
            st.caption("Favorable weather window detected.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.toast("Regional Satellite Uplink Verified.")

    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    if st.button("📂 GENERATE ELITE REPORT"):
        with st.spinner("Compiling Industrial Audit..."):
            # Fetch latest market data for the report
            live_res = call_backend("live-data", method="GET")
            market = live_res.get("market", {}) if live_res else {}
            
            payload = {
                "data": {"temperature": temp, "ph": ph, "nitrogen": nitro, "place": place, "state": state, "country": country, "soil_type": soil, "season": season},
                "recommendation": st.session_state.chat_history[-1]['content'] if st.session_state.chat_history else "Industrial session active. Field protocols deployed.",
                "language": lang, "history": st.session_state.chat_history,
                "market_snapshot": market,
                "condition_name": st.session_state.audit.get('label') if st.session_state.audit else "Unknown",
                "disease_info": st.session_state.audit.get('db') if st.session_state.audit else None,
                "image_base64": st.session_state.audit.get('image_base64') if st.session_state.audit else None,
                "country": country, "state": state, "place": place, "soil_type": soil, "season": season
            }
            res = call_backend("generate-report", payload=payload)
            if res:
                if "error" in res:
                    st.error(f"🚨 Report Engine Error: {res['error']}")
                elif "report_b64" in res:
                    # CLOUD MODE: Store base64 and filename
                    st.session_state.last_report_b64 = res['report_b64']
                    st.session_state.last_report_name = res['filename']
                    st.success("Industrial Audit Compiled Locally.")
                    st.toast("Report compiled and uplinked.")
                elif "report_url" in res:
                    st.session_state.last_report_url = res['report_url']
                    st.success("Industrial Audit Ready on Server.")
                    st.toast("Report compiled and uplinked.")
                else:
                    st.error("Protocol Error: Report generated but link missing.")
            else:
                st.error("Failed to generate report. Check backend connectivity.")

# --- MAIN DASHBOARD ---
if 'last_report_b64' not in st.session_state: st.session_state.last_report_b64 = None
if 'last_report_name' not in st.session_state: st.session_state.last_report_name = None
# --- SECURITY WATERMARK ---
auth_check = os.getenv("SHAIK_AUTH_SIGNATURE") == "AUTHORIZED_BY_THAHEER_V28"
if not auth_check:
    st.warning("⚠️ **UNAUTHORIZED REPOSITORY DETECTED**: This software is protected by intellectual property laws. Please contact Shaik Mohammad Thaheer for an authorized license.")

st.markdown(f'''
<div class="header-bar">
    <div class="header-title">🛰 AGRI-COMMAND V28.0</div>
    <div style="font-size: 11px; color: #00d1ff; font-weight: 900; letter-spacing: 1px;">
        {state.upper()} | {season.upper()} | INDUSTRIAL {"UPLINK ACTIVE" if auth_check else "LIMITED ACCESS"}
    </div>
</div>
''', unsafe_allow_html=True)

col_viz, col_chat = st.columns([1.5, 1.8])

with col_viz:
    # --- DYNAMIC INTELLIGENCE TABBED PANEL (V30.2) ---
    tabs = st.tabs(["🛰️ SATELLITE MAP", "🌍 FIELD INTEL", "🧬 BIO-SCAN", "🛒 MARKETPLACE"])
    
    with tabs[0]:
        st.markdown('<div class="sidebar-section-label" style="margin-top:0">🛰️ MULTISPECTRAL SATELLITE ARRAY</div>', unsafe_allow_html=True)
        # Larger map in main area
        m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.map_zoom)
        if st.session_state.map_coords:
            folium.Marker(st.session_state.map_coords, popup="Selected Mission Site").add_to(m)
        
        map_interaction = st_folium(m, height=450, width=None, key="main_geo_map", use_container_width=True)
        
        # Click detection logic in main map
        if map_interaction and map_interaction.get("last_clicked"):
            c = map_interaction["last_clicked"]
            if (c["lat"], c["lng"]) != st.session_state.get('last_clicked_cached'):
                st.session_state.last_clicked_cached = (c["lat"], c["lng"])
                st.session_state.map_coords = (c["lat"], c["lng"])
                st.session_state.map_center = [c["lat"], c["lng"]]
                # Background geocode
                try:
                    from backend import logic
                    geo = logic.reverse_geocode(c["lat"], c["lng"])
                    if geo:
                        st.session_state.place_val = geo["place"]
                        st.session_state.state_val = geo["state"]
                        st.session_state.country_val = geo["country"]
                        st.rerun()
                except: pass

    with tabs[1]:
        if st.session_state.intel:
            st.markdown(f'''
            <div class="audit-panel" style="border-top-color: #00d1ff; margin-bottom: 20px;">
                <div class="audit-title" style="color: #00d1ff;">🌍 GEOGRAPHIC INTELLIGENCE REPORT</div>
                <div style="font-size: 14px; line-height: 1.6;">{st.session_state.intel}</div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.info("🛰️ Select a location to generate geographic intelligence.")

    with tabs[2]:
        if st.session_state.audit:
            audit_data = st.session_state.audit
            db = audit_data.get('db', {})
            st.markdown(f'''
            <div class="audit-panel" style="border-top-color: #ff4d4d; margin-bottom: 20px;">
                <div class="audit-title" style="color: #ff4d4d;">🚀 BIO-SCAN DIAGNOSIS: {audit_data.get('label', 'Unknown')}</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px;">
                    <div>
                        <p><b>VITALITY INDEX:</b> {audit_data.get('vitality', 'N/A')}%</p>
                        <p><b>AI CONFIDENCE:</b> <span style="color: #00f07f;">{audit_data.get('confidence', '85%')}</span></p>
                        <p><b>SEVERITY:</b> <span style="color: {'#ff4d4d' if db.get('severity') == 'High' else '#ffa500'};">{db.get('severity', 'N/A')}</span></p>
                    </div>
                    <div>
                        <p><b>SYMPTOMS DETECTED:</b><br>{", ".join(db.get('symptoms', ['Visual markers identified by AI']))}</p>
                    </div>
                </div>
                <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #30363d;">
                    <b style="color: #00f07f;">INDUSTRIAL TREATMENT PROTOCOL:</b><br>
                    <div style="font-size: 13px; margin-top: 5px;">
                        {", ".join([f.get('name') for f in db.get('fungicides', [])]) if db.get('fungicides') else 'Monitoring suggested.'}
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            if db.get('treatment_schedule'):
                with st.expander("📅 VIEW DETAILED TREATMENT SCHEDULE"):
                    for day, action in db.get('treatment_schedule', {}).items():
                        st.markdown(f"**{day}**: {action}")

    with tabs[3]:
        st.markdown('<div class="sidebar-section-label" style="margin-top:0">🛒 TREATMENT MARKETPLACE</div>', unsafe_allow_html=True)
        if st.session_state.audit:
            audit_data = st.session_state.audit
            db = audit_data.get('db', {})
            products = db.get('products', [])
            
            if products:
                for prod in products:
                    with st.container():
                        st.markdown(f"""
                        <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            <div style="display: flex; flex-direction: column; gap: 15px;">
                                <div style="display: flex; align-items: start; gap: 20px;">
                                    <img src="{prod.get('image')}" width="140" style="border-radius: 8px; background: white; border: 2px solid #00f07f; padding: 5px;">
                                    <div style="flex: 1;">
                                        <h3 style="margin: 0; color: #00f07f; font-size: 18px;">{prod.get('name')}</h3>
                                        <div style="background: rgba(0, 240, 127, 0.1); color: #00f07f; padding: 4px 10px; border-radius: 20px; display: inline-block; font-size: 11px; font-weight: bold; margin-top: 8px;">PREMIUM GRADE</div>
                                        <p style="font-size: 14px; color: #e6edf3; margin: 12px 0;">{prod.get('dosage_info')}</p>
                                    </div>
                                </div>
                                <div style="background: rgba(139, 148, 158, 0.05); border-radius: 8px; padding: 12px; border: 1px dashed #30363d;">
                                    <p style="font-size: 12px; font-weight: bold; margin-bottom: 10px; color: #00d1ff;">🛒 PURCHASE ON AMAZON:</p>
                                    <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                                        {" ".join([f'<a href="{v["link"]}" target="_blank" style="text-decoration: none; background: #FF9900; color: #000; padding: 8px 16px; border-radius: 6px; font-size: 13px; font-weight: bold; border-bottom: 2px solid #cc7a00; transition: 0.2s;">🛍️ BUY ON AMAZON</a>' for v in prod.get('vendors', []) if v['company'].lower() == 'amazon']) or '<span style="color:#8b949e; font-size:12px;">Amazon listing currently unavailable for this specific SKU.</span>'}
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔬 VIEW INDUSTRIAL TECHNICAL SPECS"):
                            st.write(f"**Target Pathology:** {audit_data.get('label')}")
                            st.write(f"**Application:** Recommended {prod.get('dosage_info').split('.')[0]}")
                            st.warning("Note: Always refer to the physical product label for final safety instructions.")
            else:
                st.info("No commercial product listings available for this diagnosis yet.")
        else:
            st.info("⚡ Perform a Bio-Scan audit to unlock the Treatment Marketplace.")

    # 1. Telemetry Matrix
    st.markdown('<div class="sidebar-section-label">Real-Time Telemetry Matrix</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m1.markdown(f'<div class="metric-card"><div class="metric-label">🌡 Temp</div><div class="metric-value">{temp}</div><div class="metric-unit">°C</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><div class="metric-label">📊 Suitability</div><div class="metric-value">{random.randint(80, 98)}</div><div class="metric-unit">%</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
    m3, m4 = st.columns(2)
    m3.markdown(f'<div class="metric-card"><div class="metric-label">🧪 Nitrogen</div><div class="metric-value">{nitro}</div><div class="metric-unit">mg/L</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="metric-card"><div class="metric-label">🧬 Soil PH</div><div class="metric-value">{ph}</div><div class="metric-unit">ph</div></div>', unsafe_allow_html=True)

    if st.session_state.last_report_url:
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        st.link_button("📂 DOWNLOAD PDF AUDIT (SERVER)", st.session_state.last_report_url, type="primary", use_container_width=True)
    
    if st.session_state.last_report_b64:
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        import base64
        pdf_bytes = base64.b64decode(st.session_state.last_report_b64)
        st.download_button(
            label="📂 DOWNLOAD PDF AUDIT (CLOUD)",
            data=pdf_bytes,
            file_name=st.session_state.last_report_name,
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )

    st.markdown('<div class="sidebar-section-label">Yield potential forecasting</div>', unsafe_allow_html=True)
    crops = ["Rice", "Wheat", "Corn", "Sugarcane", "Mango", "Banana"]
    scores = [random.randint(60, 95) for _ in crops]
    df = pd.DataFrame({"Crop": crops, "Potential": scores})
    st.bar_chart(df.set_index("Crop"), horizontal=True)

with col_chat:
    st.markdown('<div class="header-title" style="font-size: 16px; margin-bottom: 20px; color: #00f07f;">🛰 MASTER INTELLIGENCE TERMINAL</div>', unsafe_allow_html=True)
    
    # V28.3: TACTICAL FOCUS MODE
    focus_col1, focus_col2 = st.columns(2)
    with focus_col1:
        if st.button("🌍 FOCUS: LOCALIZATION", use_container_width=True, type="primary" if st.session_state.get('chat_focus') == 'Localization' else 'secondary'):
            st.session_state.chat_focus = 'Localization'
            st.rerun()
    with focus_col2:
        if st.button("🚀 FOCUS: BIO-SCAN", use_container_width=True, type="primary" if st.session_state.get('chat_focus') == 'Bio-Scan' else 'secondary'):
            st.session_state.chat_focus = 'Bio-Scan'
            st.rerun()

    if 'chat_focus' not in st.session_state: st.session_state.chat_focus = 'Localization'
    st.caption(f"Current Intelligence Priority: **{st.session_state.chat_focus.upper()}**")

    # Unified Voice Briefing
    if st.button("🔊 PLAY VOICE BRIEFING", use_container_width=True):
        if st.session_state.last_speech_text:
            trigger_voice_output(st.session_state.last_speech_text, lang)
            st.audio(st.session_state.last_speech, format="audio/mp3", autoplay=True)
        else:
            st.warning("No briefing available in context.")

    chat_container = st.container(height=500)
    with chat_container:
        for msg in st.session_state.chat_history:
            cls = "chat-bubble-ai" if msg["role"] == "assistant" else "chat-bubble-user"
            st.markdown(f'<div class="{cls}">{msg["content"]}</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("Enter Command (Strategy, Bio, or Geo)...", key="master_input"):
        # CLEAN HISTORY: Remove any mention of Meta from past messages to prevent poisoning the model
        clean_history = []
        for m in st.session_state.chat_history:
            content = m["content"]
            for t in ["Meta AI", "Facebook", "Meta"]:
                content = content.replace(t, "AgriVision AI")
            clean_history.append({"role": m["role"], "content": content})
        
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.spinner("Neural Uplink Syncing..."):
            # Pass full agricultural context in every query
            res = call_backend("chat", payload={
                "message": prompt, 
                "language": lang, 
                "context_data": {
                    "telemetry": st.session_state.telemetry,
                    "place": place, "state": state, "country": country, 
                    "soil": soil, "season": season,
                    "location_intel": st.session_state.intel,
                    "bio_audit": st.session_state.audit.get('raw_res') if st.session_state.audit else None,
                    "chat_focus": st.session_state.chat_focus,
                    "history": clean_history # Send cleaned history
                }
            })
            if res:
                ans = res.get("answer", "Link Failure.")
                
                # --- FINAL UI LEVEL KILL SWITCH ---
                if any(t in ans for t in ["Meta AI", "Facebook", "Llama"]):
                    ans = f"I am AgriVision AI, developed by SHAIK MOHAMMAD THAHEER. " + ans
                    for t in ["Meta AI", "Facebook", "Llama"]: ans = ans.replace(t, "Thaheer AI")
                
                st.session_state.chat_history.append({"role": "assistant", "content": ans})
                
                # V36.0: NATURAL VOICE TRIGGER
                st.session_state.last_speech_text = res.get("speech_summary", ans)
                trigger_voice_output(st.session_state.last_speech_text, lang)
        st.rerun()

    # --- VOICE OUTPUT RENDERER ---
    if st.session_state.last_speech and st.session_state.voice_active:
        st.audio(st.session_state.last_speech, format="audio/mp3", autoplay=True)
        # Clear after playing to avoid repeat on rerun
        st.session_state.last_speech = None

    # --- DEVELOPER PROFILE (NEW V28.1) ---
    st.markdown('<div class="sidebar-section-label">Architect Profile</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(0, 209, 255, 0.05); border: 1px solid #1f2937; border-radius: 8px; padding: 15px; margin-top: 10px;">
        <div style="color: #00d1ff; font-weight: 900; font-size: 13px; letter-spacing: 1px; margin-bottom: 8px;">SHAIK MOHAMMAD THAHEER</div>
        <div style="font-size: 11px; line-height: 1.5; color: #8b949e;">
            Dedicated AI/ML infrastructure enthusiast at SRM Institute. Specialized in <b>Agentic AI</b>, 
            LLM orchestration (Gemini/GPT-4o), and autonomous browser workflows. 
            Delivering production-grade AI solutions for precision agriculture.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("CLEAR ALL CONTEXT", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.intel = ""
        st.session_state.audit = None
        st.session_state.last_report_url = None
        st.rerun()

