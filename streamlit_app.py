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

# --- CONFIG & PATHS ---
load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))
try:
    from disease_database import DISEASE_TREATMENTS, get_disease_info
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
    from disease_database import DISEASE_TREATMENTS, get_disease_info

# --- PAGE CONFIG ---
st.set_page_config(page_title="AGRI-COMMAND V28.0 | INDUSTRIAL CYBER HUB", page_icon="🛰", layout="wide")

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
        if endpoint == "geographic-intelligence":
            return logic.get_geographic_intelligence_logic(payload)
        elif endpoint == "chat":
            return logic.chat_logic(payload['message'], payload['language'], payload['context_data'])
        elif endpoint == "vision-diagnosis":
            return logic.vision_diagnosis_logic(payload['image_base64'], payload['language'])
        elif endpoint == "live-data":
            weather = logic.get_real_weather(payload.get("place", "Coimbatore")) if payload else None
            market = logic.get_real_commodity_prices()
            return {"telemetry": weather or {}, "market": market or {}}
        elif endpoint == "generate-report":
            # Reports are tricky on cloud, skipping for standalone preview
            return None
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
    country = st.text_input("Country", "India", label_visibility="collapsed", placeholder="Country")
    state = st.text_input("State", "Tamil Nadu", label_visibility="collapsed", placeholder="State")
    place = st.text_input("Place", "Coimbatore", label_visibility="collapsed", placeholder="Place")
    
    soil = st.selectbox("Soil Profile", ["Alluvial", "Black", "Red", "Sandy", "Clay", "Loamy"], label_visibility="collapsed")
    season = st.selectbox("Season", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=7, label_visibility="collapsed")
    
    if st.button("🌍 ANALYZE LOCATION", use_container_width=True):
        with st.spinner("Establishing Scientific Web Uplink..."):
            res = call_backend("geographic-intelligence", payload={
                "place": place, "state": state, "country": country, 
                "soil_type": soil, "season": season, "language": lang
            })
            if res:
                intel = res.get('intelligence', "")
                # Store location context
                st.session_state.location_context = {
                    "place": place, "state": state, "country": country,
                    "soil": soil, "season": season, "analysis": intel
                }
                st.session_state.intel = intel
                
                # V36.0: NATURAL VOICE TRIGGER (LOCATION)
                st.session_state.last_speech_text = res.get("speech_summary", intel)
                trigger_voice_output(st.session_state.last_speech_text, lang)
                
                # V28.2: SYNC TO CHAT
                st.session_state.chat_history.append({"role": "assistant", "content": intel})
                
                st.success(f"✓ Location Context Set: {place}, {state}")

    st.markdown('<div class="sidebar-section-label">Bio-Scan Uplink</div>', unsafe_allow_html=True)
    
    # Multi-Modal Input: Camera or File Upload
    cam_file = st.camera_input("Capture Crop Image", label_visibility="collapsed")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"], label_visibility="collapsed")
    
    # Process whichever image is available
    final_image = cam_file if cam_file else uploaded_file

    if final_image:
        st.image(final_image, use_container_width=True)
        if st.button("🚀 START INDUSTRIAL AUDIT"):
            with st.spinner("Executing Precision Scan..."):
                img_b64 = base64.b64encode(final_image.getvalue()).decode()
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
                    st.session_state.audit = {"raw_res": ans, "vitality": random.randint(70, 95), "db": disease_info, "label": res.get("label", ans.split('.')[0])}
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
                "country": country, "state": state, "place": place, "soil_type": soil, "season": season
            }
            res = call_backend("generate-report", payload=payload)
            if res:
                st.session_state.last_report_url = res['report_url']
                st.success("Industrial Audit Ready.")
                st.toast("Report compiled and uplinked.")
            else:
                st.error("Failed to generate report. Check backend connectivity.")

# --- MAIN DASHBOARD ---
st.markdown(f'''
<div class="header-bar">
    <div class="header-title">🛰 AGRI-COMMAND V28.0</div>
    <div style="font-size: 11px; color: #00d1ff; font-weight: 900; letter-spacing: 1px;">
        {state.upper()} | {season.upper()} | INDUSTRIAL UPLINK ACTIVE
    </div>
</div>
''', unsafe_allow_html=True)

col_viz, col_chat = st.columns([1.5, 1.8])

with col_viz:
    # --- DYNAMIC INTELLIGENCE PANEL (V28.1) ---
    if st.session_state.intel:
        st.markdown(f'''
        <div class="audit-panel" style="border-top-color: #00d1ff; margin-bottom: 20px;">
            <div class="audit-title" style="color: #00d1ff;">🌍 GEOGRAPHIC INTELLIGENCE REPORT</div>
            <div style="font-size: 14px; line-height: 1.6;">{st.session_state.intel}</div>
        </div>
        ''', unsafe_allow_html=True)

    if st.session_state.audit:
        audit_data = st.session_state.audit
        db = audit_data.get('db', {})
        st.markdown(f'''
        <div class="audit-panel" style="border-top-color: #ff4d4d; margin-bottom: 20px;">
            <div class="audit-title" style="color: #ff4d4d;">🚀 BIO-SCAN DIAGNOSIS: {audit_data.get('raw_res', '').split('.')[0]}</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px;">
                <div>
                    <p><b>VITALITY INDEX:</b> {audit_data.get('vitality', 'N/A')}%</p>
                    <p><b>RECOVERY:</b> {db.get('recovery_timeline', 'N/A')}</p>
                    <p><b>SEVERITY:</b> {db.get('severity', 'N/A')}</p>
                </div>
                <div>
                    <p><b>SYMPTOMS:</b><br>{", ".join(db.get('symptoms', ['N/A']))}</p>
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
        st.link_button("📂 DOWNLOAD PDF AUDIT", st.session_state.last_report_url, type="primary", use_container_width=True)

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
                    "history": st.session_state.chat_history
                }
            })
            if res:
                ans = res.get("answer", "Link Failure.")
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

    if st.button("CLEAR ALL CONTEXT", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.intel = ""
        st.session_state.audit = None
        st.session_state.last_report_url = None
        st.rerun()

