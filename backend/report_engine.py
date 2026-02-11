from fpdf import FPDF
import datetime
import os
import logging
import base64
import re

logger = logging.getLogger("AGRI_V14_REPORT")

class EliteAgriReportV14:
    def __init__(self, output_dir="reports"):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(curr_dir, output_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
        
        # Font Search (V16.0: Enhanced style mapping)
        self.fonts = {"": None, "B": None}
        self.font_family = "NirmalaUI"
        
        # Try finding Nirmala (UI or Regular)
        n_reg = "C:/Windows/Fonts/Nirmala.ttf"
        n_bold = "C:/Windows/Fonts/NirmalaB.ttf"
        g_reg = "C:/Windows/Fonts/Gautami.ttf"
        
        if os.path.exists(n_reg):
            self.fonts[""] = n_reg
            if os.path.exists(n_bold): self.fonts["B"] = n_bold
            self.font_family = "Nirmala"
        elif os.path.exists(g_reg):
            self.fonts[""] = g_reg
            self.font_family = "Gautami"
            
        self.unicode_supported = self.fonts[""] is not None

    def clean_text(self, text, allow_unicode=False):
        if not text: return ""
        text = str(text)
        # Remove common markdown symbols
        for char in ['*', '_', '#', '`']:
            text = text.replace(char, '')
        
        if allow_unicode:
            return text
        
        # ELITE SAFETY: Pure ASCII fallback
        # This prevents any 'latin-1' or other encoding crashes with standard fonts
        return "".join([c if ord(c) < 128 else "" for c in text])

    def generate_report(self, data, recommendation, sector="Global", history=None, image_base64=None, condition_name="Unknown", language="English", disease_info=None, crop_scores=None):
        """V14.0 Elite Business Audit with Enhanced Disease Treatment Section"""
        try:
            pdf = FPDF()
            # V36.0: Global Font Safety
            use_unicode = self.unicode_supported and language != "English"
            font_main = "Helvetica"
            font_size_header = 18
            
            if use_unicode:
                try:
                    pdf.add_font(self.font_family, "", self.fonts[""])
                    # Always register styles to prevent "Undefined font" errors
                    # Map Bold
                    if self.fonts["B"]: pdf.add_font(self.font_family, "B", self.fonts["B"])
                    else: pdf.add_font(self.font_family, "B", self.fonts[""])
                    
                    # Map Italic and Bold-Italic to Regular for maximum safety
                    pdf.add_font(self.font_family, "I", self.fonts[""])
                    pdf.add_font(self.font_family, "BI", self.fonts["B"] if self.fonts["B"] else self.fonts[""])
                    
                    font_main = self.font_family
                except Exception as fe:
                    logger.warning(f"Font Load Failed: {fe}")
                    use_unicode = False
            
            pdf.add_page()
            
            def safe_cell(w, h=0, txt="", border=0, ln=0, align='', fill=False, link=''):
                pdf.cell(w, h, self.clean_text(txt, use_unicode), border, ln, align, fill, link)
            
            def safe_multi_cell(w, h, txt, border=0, align='J', fill=False):
                pdf.multi_cell(w, h, self.clean_text(txt, use_unicode), border, align, fill)

            # --- HEADER ---
            pdf.set_font(font_main, 'B', font_size_header)
            pdf.set_text_color(10, 30, 80)
            
            v15_titles = {
                "English": "AGRI-COMMAND V20.0: INDUSTRIAL MASTER HUB",
                "Tamil": "வேளாண்-கட்டளை V20.0: தொழில்துறை தலைமை மையம்",
                "Hindi": "कृषि-कमांड V20.0: इंडस्ट्रियल मास्टर हब",
                "Telugu": "అగ్రి-కమాండ్ V20.0: ఇండస్ట్రియల్ మాస్టర్ హబ్",
                "Urdu": "ایگری کمانڈ V20.0: صنعتی ماسٹر حب",
                "Malayalam": "അഗ്രി-കമാൻഡ് V20.1: ഇൻഡസ്ട്രിയൽ മാസ്റ്റർ ഹബ്"
            }
            safe_cell(0, 15, v15_titles.get(language, v15_titles["English"]), ln=True, align='L')
            
            pdf.set_font(font_main, size=9)
            pdf.set_text_color(100, 100, 100)
            data_source = data.get("data_source", "SATELLITE_FEED")
            auth_str = f"SECTOR: {sector.upper()} | AUTH: BIOMETRIC_VERIFIED | DATA: {data_source} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            safe_cell(0, 8, auth_str, ln=True, align='L')
            pdf.ln(5)

            # --- I. VISUAL BIOLOGICAL DIAGNOSIS ---
            pdf.set_font(font_main, 'B', 12)
            pdf.set_text_color(0, 0, 0)
            safe_cell(190, 10, "I. VISUAL BIOLOGICAL DIAGNOSIS & TREATMENT PROTOCOL", border="B", ln=True)
            pdf.ln(3)
            
            pdf.set_font(font_main, 'B', 10)
            pdf.set_text_color(150, 0, 0)
            safe_cell(0, 8, f"DETECTED CONDITION: {condition_name.upper()}", ln=True)
            
            if image_base64:
                try:
                    img_data = base64.b64decode(image_base64)
                    temp_img = os.path.join(self.output_dir, f"diag_{datetime.datetime.now().strftime('%H%M%S')}.jpg")
                    with open(temp_img, "wb") as f: f.write(img_data)
                    # Center the image
                    pdf.image(temp_img, x=60, y=pdf.get_y(), w=80)
                    pdf.set_y(pdf.get_y() + 65)
                except: pass
            
            # V14.0: Enhanced Disease Treatment Section
            if disease_info and disease_info.get("severity") != "Unknown":
                pdf.set_font(font_main, 'B', 10)
                pdf.set_text_color(0, 0, 0)
                sev = disease_info.get('severity', 'Unknown')
                timeline = disease_info.get('recovery_timeline', 'Consult expert')
                safe_cell(0, 7, f"SEVERITY: {sev}", ln=True)
                safe_cell(0, 7, f"RECOVERY TIMELINE: {timeline}", ln=True)
                pdf.ln(2)
                
                # Recommended Fungicides
                pdf.set_font(font_main, 'B', 10)
                pdf.set_text_color(0, 102, 51)
                safe_cell(0, 7, "RECOMMENDED CHEMICAL TREATMENTS:", ln=True)
                pdf.set_font(font_main, size=9)
                pdf.set_text_color(0, 0, 0)
                
                for idx, fungicide in enumerate(disease_info.get("fungicides", [])[:3], 1):
                    pdf.set_font(font_main, 'B', 9)
                    name = fungicide.get('name', 'N/A')
                    safe_cell(10); safe_cell(0, 6, f"{idx}. {name}", ln=True)
                    pdf.set_font(font_main, size=8)
                    
                    ai = fungicide.get('active_ingredient', 'N/A')
                    dosage = fungicide.get('dosage', 'N/A')
                    app = fungicide.get('application', 'N/A')
                    brands = ", ".join(fungicide.get('brands', ['N/A']))
                    
                    pdf.cell(20); safe_cell(0, 5, f"Active Ingredient: {ai}", ln=True)
                    pdf.cell(20); safe_cell(0, 5, f"Dosage: {dosage}", ln=True)
                    pdf.cell(20); safe_cell(0, 5, f"Application: {app}", ln=True)
                    pdf.cell(20); safe_cell(0, 5, f"Brands: {brands}", ln=True)
                    pdf.ln(1)
                
                # Treatment Schedule
                if disease_info.get("treatment_schedule"):
                    pdf.set_font(font_main, 'B', 10)
                    pdf.set_text_color(0, 51, 153)
                    safe_cell(0, 7, "APPLICATION SCHEDULE:", ln=True)
                    pdf.set_font(font_main, size=8)
                    pdf.set_text_color(0, 0, 0)
                    for day, action in disease_info.get("treatment_schedule", {}).items():
                        pdf.cell(10); safe_cell(0, 5, f"{day}: {action}", ln=True)
                    pdf.ln(2)
                
                # Safety Precautions
                if disease_info.get("safety_precautions"):
                    pdf.set_font(font_main, 'B', 10)
                    pdf.set_text_color(153, 0, 0)
                    safe_cell(0, 7, "SAFETY PRECAUTIONS:", ln=True)
                    pdf.set_font(font_main, size=8)
                    pdf.set_text_color(0, 0, 0)
                    for precaution in disease_info.get("safety_precautions", [])[:4]:
                        pdf.cell(10); safe_cell(0, 5, f"- {precaution}", ln=True)
            
            pdf.ln(5)

            # --- II. MARKET INTELLIGENCE ---
            pdf.set_font(font_main, 'B', 12)
            pdf.set_text_color(0, 0, 0)
            safe_cell(190, 10, "II. MARKET INTELLIGENCE & PRICE VARIANCE", border="B", ln=True)
            pdf.ln(3)
            
            pdf.set_font(font_main, size=10)
            market = data.get("market_snapshot", {})
            if not market:
                pdf.set_text_color(100, 100, 100)
                safe_cell(0, 7, "No live market data for this sector. Using global commodities index.", ln=True)
            else:
                for crop, specs in market.items():
                    pdf.set_text_color(0, 0, 0)
                    safe_cell(60, 7, f"{crop} Global Index:", border=0)
                    price = specs.get('price', 0)
                    change = specs.get('change', 0)
                    col = (0, 120, 0) if change >= 0 else (180, 0, 0)
                    pdf.set_text_color(*col)
                    safe_cell(40, 7, f"${price} ({'+' if change>=0 else ''}{change}%)", border=0)
                    pdf.set_text_color(100, 100, 100)
                    safe_cell(0, 7, f" Status: {'BULLISH' if change >= 0 else 'BEARISH'}", ln=True)
            pdf.ln(5)

            # --- III. CLIMATE INTELLIGENCE & ENVIRONMENTAL CONTEXT ---
            pdf.set_font(font_main, 'B', 12)
            pdf.set_text_color(0, 0, 0)
            safe_cell(190, 10, "III. CLIMATE INTELLIGENCE & ENVIRONMENTAL CONTEXT", border="B", ln=True)
            pdf.ln(3)
            
            pdf.set_font(font_main, 'B', 9)
            pdf.set_fill_color(240, 240, 245)
            safe_cell(190, 8, " ENVIRONMENTAL CONTEXT SUMMARY", border=1, fill=True, ln=True)
            pdf.set_font(font_main, size=8)
            pdf.set_text_color(50, 50, 50)
            
            safe_cell(63, 7, f" Location: {data.get('place', 'N/A')}", border=1)
            safe_cell(63, 7, f" Season: {data.get('season', 'N/A')}", border=1)
            safe_cell(64, 7, f" Soil Type: {data.get('soil_type', 'N/A')}", border=1, ln=True)
            pdf.ln(2)

            pdf.set_font(font_main, size=10)
            pdf.set_text_color(0, 0, 0)
            temp = data.get("temperature", 28.5)
            hum = data.get("humidity", 55)
            risk_lvl = "LOW" if 20 <= temp <= 30 and hum < 70 else "ELEVATED"
            trends = f"Seasonal trends for {data.get('season', 'August')} suggest {'stable' if risk_lvl == 'LOW' else 'unstable'} growth conditions."
            safe_multi_cell(190, 6, f"Thermal state detected at {temp}C with {hum}% relative humidity. Bio-Risk Index is currently {risk_lvl}. " + trends)
            pdf.ln(5)

            # --- IV. FIELD TELEMETRY & BIOLOGICAL INDICES ---
            pdf.set_font(font_main, 'B', 12)
            pdf.set_text_color(0, 0, 0)
            safe_cell(190, 10, "IV. FIELD TELEMETRY & BIOLOGICAL INDICES", border="B", ln=True)
            pdf.ln(3)
            
            pdf.set_fill_color(230, 230, 235)
            pdf.set_font(font_main, 'B', 10)
            safe_cell(95, 10, " Sensor Category", border=1, fill=True)
            safe_cell(95, 10, " Measured Value", border=1, fill=True, ln=True)
            
            pdf.set_font(font_main, size=10)
            metrics = [
                ("Temperature", f"{data.get('temperature', '28.5')} C"),
                ("Humidity", f"{data.get('humidity', '55')}%"),
                ("Dissolved Oxygen", f"{data.get('dissolved_oxygen', '6.5')} mg/L"),
                ("Nitrogen (N)", f"{data.get('nitrogen', '2.5')} mg/L"),
                ("Phosphorus (P)", f"{data.get('phosphorus', 'N/A')} mg/L"),
                ("Potassium (K)", f"{data.get('potassium', 'N/A')} mg/L"),
                ("Soil PH", f"{data.get('ph', '6.5')}")
            ]
            for label, val in metrics:
                safe_cell(95, 8, f" {label}", border=1)
                safe_cell(95, 8, f" {val}", border=1, ln=True)
            pdf.ln(5)

            # --- V. STRATEGIC INDUSTRIAL RECOMMENDATION ---
            pdf.add_page()
            pdf.set_font(font_main, 'B', 12)
            pdf.set_text_color(0, 0, 0)
            safe_cell(190, 10, "V. STRATEGIC INDUSTRIAL RECOMMENDATION", border="B", ln=True)
            pdf.ln(5)
            
            pdf.set_font(font_main, size=10)
            pdf.set_text_color(20, 20, 20)
            # Use larger line height and wrap for cleaner content
            safe_multi_cell(190, 8, recommendation)
            pdf.ln(5)

            # --- VI. INDUSTRIAL FERTILIZATION & NUTRIENT PROTOCOL ---
            pdf.set_font(font_main, 'B', 12)
            pdf.set_text_color(0, 0, 0)
            safe_cell(190, 10, "VI. INDUSTRIAL FERTILIZATION & NUTRIENT PROTOCOL", border="B", ln=True)
            pdf.ln(5)
            
            n_val = data.get("nitrogen", 2.5)
            fert_rec = "MAINTENANCE: Soil nutrient levels are stable. Apply NPK 19:19:19 at 5kg/acre."
            if n_val < 2.0:
                fert_rec = "CRITICAL NITROGEN DEFICIENCY: Immediate application of Urea or Liquid Ammonia recommended. Target: 15kg/acre."
            elif n_val > 4.0:
                fert_rec = "NITROGEN SURPLUS: Suspend nitrogenous fertilizers. Risk of toxicity and pest susceptibility elevated."
                
            pdf.set_font(font_main, 'B', 10)
            safe_cell(0, 7, "NUTRIENT ANALYSIS:", ln=True)
            pdf.set_font(font_main, size=10)
            safe_multi_cell(190, 7, fert_rec)
            pdf.ln(5)

            # --- VII. GEOGRAPHIC INTELLIGENCE & CROP SUITABILITY ---
            if crop_scores:
                pdf.set_font(font_main, 'B', 12)
                pdf.set_text_color(0, 0, 0)
                safe_cell(190, 10, "VII. GEOGRAPHIC INTELLIGENCE & CROP SUITABILITY", border="B", ln=True)
                pdf.ln(5)
                
                pdf.set_fill_color(235, 245, 235)
                pdf.set_font(font_main, 'B', 10)
                safe_cell(95, 10, " Crop Variety", border=1, fill=True)
                safe_cell(95, 10, " Suitability Index (%)", border=1, fill=True, ln=True)
                
                pdf.set_font(font_main, size=10)
                for crop, score in sorted(crop_scores.items(), key=lambda x: str(x[1]), reverse=True):
                    pdf.set_text_color(0, 0, 0)
                    safe_cell(95, 8, f" {crop}", border=1)
                    try:
                        f_score = float(score)
                        col = (0, 100, 0) if f_score > 70 else (100, 50, 0)
                    except:
                        col = (0, 0, 0)
                    pdf.set_text_color(*col)
                    safe_cell(95, 8, f" {score}%", border=1, ln=True)
                pdf.ln(10)

            # --- VIII. TACTICAL IRRIGATION & WATER AUDIT ---
            pdf.set_font(font_main, 'B', 12)
            pdf.set_text_color(0, 51, 102)
            safe_cell(190, 10, "VIII. TACTICAL IRRIGATION & WATER AUDIT", border="B", ln=True)
            pdf.ln(5)
            
            irrigation_advice = (
                "TACTICAL STATUS: Optimization Required. For Paddy/Sugarcane, maintain Soil Moisture between 65-80%.\n"
                "MICRO-IRRIGATION PROTOCOL: Ensure Drip emitters are flushed for salt removal.\n"
                "FERTIGATION: Switch to water-soluble NPK (19:19:19) via venturi for maximum nutrient uptake.\n"
                "PADDY FOCUS: Alternate Wetting and Drying (AWD) recommended to reduce methane and save 25% water."
            )
            pdf.set_font(font_main, size=10)
            pdf.set_text_color(0, 0, 0)
            safe_multi_cell(190, 7, irrigation_advice)
            pdf.ln(5)

            # --- IX. MISSION TRANSCRIPT & TACTICAL LOGS ---
            if history:
                pdf.add_page()
                pdf.set_font(font_main, 'B', 12)
                pdf.set_text_color(0, 0, 0)
                safe_cell(190, 10, "IX. MISSION TRANSCRIPT & TACTICAL LOGS", border="B", ln=True)
                pdf.ln(5)
                
                for entry in history[-20:]: # Last 20 messages
                    role = entry.get("role", "Unknown").upper()
                    content = entry.get("content", "")
                    
                    # Style box for role
                    is_assistant = role == "ASSISTANT"
                    pdf.set_font(font_main, 'B', 9)
                    pdf.set_text_color(0, 100, 150) if is_assistant else pdf.set_text_color(51, 51, 51)
                    safe_cell(0, 8, f"[{role}]:", ln=True)
                    
                    pdf.set_font(font_main, size=9)
                    pdf.set_text_color(0, 0, 0)
                    # Use slight indent for content
                    pdf.set_x(15)
                    safe_multi_cell(175, 6, content)
                    pdf.ln(3)

            pdf.ln(10)
            pdf.set_y(-20)
            pdf.set_font(font_main, 'I', 8)
            pdf.set_text_color(150, 150, 150)
            safe_cell(0, 10, f"Agri-Command V20.0 | Industrial Master Hub | AI-Generated Audit Report | Localized: {language}", align='C')

            filename = f"Industrial_Audit_{language}_{datetime.datetime.now().strftime('%Y%p%m_%H%M%S')}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            pdf.output(filepath)
            return filepath, filename
            
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            logger.error(f"Elite Report Crash: {e}\n{error_trace}")
            print(f"REPORT ENGINE CRASH: {e}\n{error_trace}") # Print to stdout as well
            try:
                emer = FPDF()
                emer.add_page(); emer.set_font("Helvetica", 'B', 14)
                emer.cell(0, 10, "V15.0 EMERGENCY DATA RECOVERY", ln=True)
                emer.set_font("Helvetica", size=9)
                # Final fallback: strip EVERYTHING non-ascii
                error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
                # Use fixed width 190 to avoid "horizontal space" crash
                emer.multi_cell(190, 7, f"Formatting Error: {error_msg}\nRecommendation summary below (ASCII only):")
                safe_rec = str(recommendation).encode('ascii', 'ignore').decode('ascii')
                emer.multi_cell(190, 7, safe_rec)
                fpath = os.path.join(self.output_dir, f"Emergency_{datetime.datetime.now().strftime('%H%M%S')}.pdf")
                emer.output(fpath)
                return fpath, os.path.basename(fpath)
            except Exception as final_e: 
                logger.critical(f"FATAL REPORT ERROR: {final_e}")
                raise RuntimeError(str(final_e))

report_engine = EliteAgriReportV14()
