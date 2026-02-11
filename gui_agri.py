import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import requests
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from collections import deque
import numpy as np
import time
import webbrowser
import pyttsx3
import base64
import random
from PIL import Image, ImageTk
from io import BytesIO

class UltimateAgriCommandV14(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AGRI-COMMAND V20.0 | INDUSTRIAL MASTER HUB")
        self.geometry("1440x920") # Slightly taller for geo-inputs
        self.configure(bg="#05070a")

        self.colors = {
            "bg": "#05070a", "panel": "#0c1117", "sidebar": "#080c12",
            "accent": "#00d1ff", "green": "#00f07f", "red": "#ff4d4d",
            "gold": "#ffd700", "text": "#e1e4e8", "dim": "#6a737d", "border": "#30363d"
        }

        self.api_base = "http://localhost:8002/api"
        self.sim_data = {
            "temperature": 28.4, "humidity": 55, "nitrogen": 2.50, 
            "phosphorus": 1.80, "potassium": 2.20, "ph": 6.5, "dissolved_oxygen": 6.50,
            "sector": "North Sector",
            "country": "India", "state": "Tamil Nadu", "place": "Coimbatore", "soil_type": "Alluvial"
        }
        self.market_data = {}
        self.geo_entries = {}
        self.chat_history = [] 
        self.last_img_base64 = ""
        self.last_condition_label = "None"
        self.last_ai_briefing = ""  
        self.voice_active = True
        self.tts_busy = False
        
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 165)
        except:
            self.tts_engine = None
        
        self.setup_styles()
        self.setup_ui()
        self.bootstrap()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="#161b22", background="#161b22", foreground="white")

    def setup_ui(self):
        # --- HEADER 🛰 ---
        self.header = tk.Frame(self, bg=self.colors["sidebar"], height=70, highlightbackground=self.colors["border"], highlightthickness=1)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        tk.Label(self.header, text="🛰 AGRI-COMMAND V20.0", bg=self.colors["sidebar"], fg="white", font=("Inter", 16, "bold")).pack(side="left", padx=25)
        
        # Text Language
        tk.Label(self.header, text="Text:", bg=self.colors["sidebar"], fg=self.colors["dim"], font=("Inter", 8)).pack(side="left")
        self.lang_var = tk.StringVar(value="English")
        self.lang_box = ttk.Combobox(self.header, textvariable=self.lang_var, values=["English", "Tamil", "Hindi", "Telugu", "Urdu", "Malayalam"], state="readonly", width=10)
        self.lang_box.pack(side="left", padx=5)
        self.lang_box.bind("<<ComboboxSelected>>", self.on_language_change)
        
        # Voice Language (V18.0 Multi-Regional)
        tk.Label(self.header, text="Voice:", bg=self.colors["sidebar"], fg=self.colors["dim"], font=("Inter", 8)).pack(side="left", padx=(10,0))
        self.voice_lang_var = tk.StringVar(value="English")
        self.voice_lang_box = ttk.Combobox(self.header, textvariable=self.voice_lang_var, values=["English", "Tamil", "Hindi", "Telugu", "Urdu", "Malayalam"], state="readonly", width=10)
        self.voice_lang_box.pack(side="left", padx=5)
        
        self.sector_var = tk.StringVar(value="North Sector")
        self.sector_box = ttk.Combobox(self.header, textvariable=self.sector_var, values=["North Sector", "South Sector", "East Sector", "West Sector", "Global Hub"], state="readonly", width=15)
        self.sector_box.pack(side="left", padx=10)

        tk.Button(self.header, text="ANALYTICS HUB", bg="#161b22", fg=self.colors["accent"], font=("Inter", 8, "bold"), relief="flat", command=self.open_analytics_window).pack(side="right", padx=15, ipady=5)

        # --- MAIN BODY ---
        self.body = tk.Frame(self, bg=self.colors["bg"])
        self.body.pack(fill="both", expand=True)

        # 1. SIDEBAR (V13.5 GEOGRAPHIC HUB)
        self.sidebar = tk.Frame(self.body, bg=self.colors["sidebar"], width=320, padx=15, pady=15, highlightbackground=self.colors["border"], highlightthickness=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        v_f = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        v_f.pack(fill="x", pady=(0, 10))
        self.v_btn = tk.Button(v_f, text="🔊 VOICE V-COM: ON", bg="#161b22", fg=self.colors["green"], font=("Inter", 9, "bold"), relief="flat", command=self.toggle_voice)
        self.v_btn.pack(fill="x")

        # Geographic Hub
        tk.Label(self.sidebar, text="🌍 GEOGRAPHIC INTELLIGENCE", bg=self.colors["sidebar"], fg=self.colors["accent"], font=("Inter", 9, "bold")).pack(anchor="w", pady=(5, 5))
        
        for lbl, key in [("Country", "country"), ("State", "state")]:
            f = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
            f.pack(fill="x", pady=2)
            tk.Label(f, text=lbl, bg=self.colors["sidebar"], fg=self.colors["dim"], font=("Inter", 7), width=6, anchor="w").pack(side="left")
            e = tk.Entry(f, bg="#0d1117", fg="white", borderwidth=0, font=("Inter", 8), insertbackground="white")
            e.insert(0, self.sim_data[key])
            e.pack(side="right", fill="x", expand=True, padx=(5, 0))
            self.geo_entries[key] = e

        # V21.0: Place Autocomplete
        f_place = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        f_place.pack(fill="x", pady=2)
        tk.Label(f_place, text="Place", bg=self.colors["sidebar"], fg=self.colors["dim"], font=("Inter", 7), width=6, anchor="w").pack(side="left")
        self.place_entry = tk.Entry(f_place, bg="#0d1117", fg="white", borderwidth=0, font=("Inter", 8), insertbackground="white")
        self.place_entry.insert(0, self.sim_data["place"])
        self.place_entry.pack(side="right", fill="x", expand=True, padx=(5, 0))
        self.geo_entries["place"] = self.place_entry
        self.place_entry.bind("<KeyRelease>", self.update_autocomplete)

        self.suggest_box = tk.Listbox(self.sidebar, bg="#161b22", fg="white", font=("Inter", 8), height=4, highlightthickness=0, borderwidth=0)
        self.suggest_box.bind("<<ListboxSelect>>", self.select_autocomplete)
        self.suggest_box.pack_forget() # Initially hidden

        f_soil = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        f_soil.pack(fill="x", pady=5)
        tk.Label(f_soil, text="Soil Type", bg=self.colors["sidebar"], fg=self.colors["dim"], font=("Inter", 7)).pack(side="left")
        self.soil_var = tk.StringVar(value="Alluvial")
        self.soil_box = ttk.Combobox(f_soil, textvariable=self.soil_var, values=["Alluvial", "Black", "Red", "Sandy", "Clay", "Loamy"], state="readonly", font=("Inter", 8), width=15)
        self.soil_box.pack(side="right")
        self.soil_box.bind("<<ComboboxSelected>>", lambda e: self.on_geo_change("soil_type", self.soil_var.get()))

        f_season = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        f_season.pack(fill="x", pady=5)
        tk.Label(f_season, text="Tactical Season", bg=self.colors["sidebar"], fg=self.colors["dim"], font=("Inter", 7)).pack(side="left")
        self.season_var = tk.StringVar(value="August")
        self.season_box = ttk.Combobox(f_season, textvariable=self.season_var, values=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], state="readonly", font=("Inter", 8), width=15)
        self.season_box.pack(side="right")
        self.season_box.bind("<<ComboboxSelected>>", lambda e: self.on_geo_change("season", self.season_var.get()))
        
        # V14.0: Geographic Intelligence Button
        tk.Button(self.sidebar, text="🌍 ANALYZE LOCATION", bg=self.colors["accent"], fg="black", font=("Inter", 9, "bold"), relief="flat", command=self.analyze_geographic_intelligence).pack(fill="x", pady=10)

        tk.Label(self.sidebar, text="📸 BIO-SCAN UPLINK", bg=self.colors["sidebar"], fg=self.colors["dim"], font=("Inter", 9, "bold")).pack(anchor="w", pady=(15, 5))
        self.vision_preview = tk.Label(self.sidebar, text="[ NO IMAGE ]", bg="#0d1117", fg=self.colors["dim"], font=("Inter", 7), width=35, height=6)
        self.vision_preview.pack(pady=5)
        self.upload_btn = tk.Button(self.sidebar, text="SCAN LEAF DATA", bg="#161b22", fg="white", font=("Inter", 8, "bold"), relief="flat", command=self.upload_and_diagnose)
        self.upload_btn.pack(fill="x", pady=5)

        tk.Label(self.sidebar, text="TELEMETRY SENSORS", bg=self.colors["sidebar"], fg=self.colors["dim"], font=("Inter", 9, "bold")).pack(anchor="w", pady=(15, 5))
        for label, key, min_v, max_v, init in [
            ("TEMP (C)", "temperature", 10, 45, 28.5),
            ("SOIL PH", "ph", 0, 14, 6.5),
            ("NITROGEN", "nitrogen", 0, 10, 2.50)
        ]:
            f = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
            f.pack(fill="x", pady=2)
            tk.Label(f, text=label, bg=self.colors["sidebar"], fg=self.colors["text"], font=("Inter", 7)).pack(side="left")
            v_lbl = tk.Label(f, text=f"{init:.2f}", bg=self.colors["sidebar"], fg=self.colors["accent"], font=("Inter", 7, "bold"))
            v_lbl.pack(side="right")
            s = ttk.Scale(self.sidebar, from_=min_v, to=max_v, orient="horizontal", command=lambda v, k=key, l=v_lbl: self.on_sim_change(k, v, l))
            s.set(init)
            s.pack(fill="x")

        tk.Button(self.sidebar, text="GENERATE ELITE REPORT", bg=self.colors["green"], fg="black", font=("Inter", 9, "bold"), relief="flat", command=self.generate_report).pack(fill="x", side="bottom", pady=5, ipady=10)

        # 2. CENTRAL INTELLIGENCE
        self.center = tk.Frame(self.body, bg=self.colors["bg"], padx=15, pady=15)
        self.center.pack(side="left", fill="both", expand=True)

        tile_f = tk.Frame(self.center, bg=self.colors["bg"])
        tile_f.pack(fill="x", pady=(0, 15))
        self.cards = {}
        for title, key, icon in [("TEMPERATURE", "temperature", "🌡"), ("SUITABILITY %", "suitability", "📈"), ("NITROGEN", "nitrogen", "💨"), ("PH LEVEL", "ph", "🧪")]:
            card = tk.Frame(tile_f, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1, padx=15, pady=15)
            card.pack(side="left", padx=10, fill="both", expand=True)
            tk.Label(card, text=f"{icon} {title}", bg=self.colors["panel"], fg=self.colors["dim"], font=("Inter", 8, "bold")).pack(anchor="w")
            self.cards[key] = tk.Label(card, text="---", bg=self.colors["panel"], fg="white", font=("Inter", 22, "bold"))
            self.cards[key].pack(anchor="w", pady=(5, 0))

        self.viz_p = tk.Frame(self.center, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1)
        self.viz_p.pack(fill="both", expand=True, padx=5)
        viz_hdr = tk.Frame(self.viz_p, bg="#161b22", height=35)
        viz_hdr.pack(fill="x")
        tk.Label(viz_hdr, text="📉 GEOGRAPHIC CROP POTENTIAL (GROWTH %)", bg="#161b22", fg=self.colors["accent"], font=("Inter", 9, "bold")).pack(side="left", padx=15)

        self.fig = plt.Figure(figsize=(6, 4))
        self.fig.patch.set_facecolor('#0c1117')
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_p)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # 3. RIGHT ADVISOR
        self.ai_pane = tk.Frame(self.body, bg=self.colors["sidebar"], width=350, padx=20, pady=20, highlightbackground=self.colors["border"], highlightthickness=1)
        self.ai_pane.pack(side="right", fill="y")
        self.ai_pane.pack_propagate(False)

        tk.Label(self.ai_pane, text="🧠 TACTICAL STRATEGIST V20.0", bg=self.colors["sidebar"], fg=self.colors["accent"], font=("Inter", 13, "bold")).pack(anchor="w")
        self.status_lbl = tk.Label(self.ai_pane, text="OPERATIONAL: READY", bg=self.colors["sidebar"], fg=self.colors["gold"], font=("Inter", 8, "bold"))
        self.status_lbl.pack(anchor="w", pady=(0, 10))

        self.chat_out = scrolledtext.ScrolledText(self.ai_pane, bg="#0d1117", fg="#ced4da", font=("Inter", 9), borderwidth=0, padx=10, pady=10, wrap="word", insertbackground="white")
        self.chat_out.pack(fill="both", expand=True)
        
        # V14.0: Clear Chat Button
        tk.Button(self.ai_pane, text="CLEAR HISTORY", bg=self.colors["red"], fg="white", font=("Inter", 8, "bold"), relief="flat", command=self.clear_chat_history).pack(fill="x", pady=(5,10))

        chat_in_f = tk.Frame(self.ai_pane, bg="#161b22", height=45)
        chat_in_f.pack(fill="x", pady=(15, 0))
        chat_in_f.pack_propagate(False)
        self.chat_in = tk.Entry(chat_in_f, bg="#161b22", fg="white", borderwidth=0, font=("Inter", 10), insertbackground="white")
        self.chat_in.pack(side="left", fill="both", expand=True, padx=(10, 5))
        self.chat_in.bind("<Return>", lambda e: self.send_ai_query())
        tk.Button(chat_in_f, text="SYNC", bg=self.colors["accent"], fg="black", font=("Inter", 9, "bold"), relief="flat", width=8, command=self.send_ai_query).pack(side="right", fill="y")

    def bootstrap(self):
        def _poll():
            while True:
                try:
                    res = requests.get(f"{self.api_base}/live-data", timeout=3)
                    if res.status_code == 200:
                        all_data = res.json()
                        self.after(0, self.update_dashboard, all_data['telemetry'], all_data['market'])
                except: pass
                time.sleep(3)
        threading.Thread(target=_poll, daemon=True).start()

    def update_autocomplete(self, event=None):
        query = self.place_entry.get().strip()
        if len(query) < 3:
            self.suggest_box.pack_forget()
            return

        def _fetch():
            try:
                url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&addressdetails=1&limit=5"
                headers = {"User-Agent": "AgriCommand/1.0"}
                res = requests.get(url, headers=headers, timeout=3)
                if res.status_code == 200:
                    suggestions = res.json()
                    self.current_suggestions = suggestions
                    self.after(0, self.show_suggestions, [s.get("display_name") for s in suggestions])
            except: pass
        
        threading.Thread(target=_fetch, daemon=True).start()

    def show_suggestions(self, names):
        if not names:
            self.suggest_box.pack_forget()
            return
        self.suggest_box.delete(0, tk.END)
        for name in names: self.suggest_box.insert(tk.END, name)
        self.suggest_box.pack(fill="x", pady=2)

    def select_autocomplete(self, event=None):
        idx = self.suggest_box.curselection()
        if not idx: return
        
        selected_data = self.current_suggestions[idx[0]]
        addr = selected_data.get("address", {})
        
        place = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("suburb") or selected_data.get("display_name").split(",")[0]
        state = addr.get("state", "")
        country = addr.get("country", "")
        
        self.place_entry.delete(0, tk.END); self.place_entry.insert(0, place)
        self.geo_entries["state"].delete(0, tk.END); self.geo_entries["state"].insert(0, state)
        self.geo_entries["country"].delete(0, tk.END); self.geo_entries["country"].insert(0, country)
        
        self.suggest_box.pack_forget()
        self.on_geo_change("place", place)
        self.on_geo_change("state", state)
        self.on_geo_change("country", country)

    def on_language_change(self, event=None):
        self.display_chat("SYS", f"Language Switched to {self.lang_var.get()}. Syncing Intelligence...")
        if self.last_img_base64: self.upload_and_diagnose(re_trigger=True)

    def on_geo_change(self, key, val):
        self.sim_data[key] = val
        requests.post(f"{self.api_base}/simulate", json=self.sim_data)
        self.update_predictor()

    def toggle_voice(self):
        self.voice_active = not self.voice_active
        if not self.voice_active:
            self.stop_voice()
            self.v_btn.config(text="🔇 VOICE V-COM: OFF", fg=self.colors["dim"])
        else:
            self.v_btn.config(text="🔊 VOICE V-COM: ON", fg=self.colors["green"])

    def stop_voice(self):
        if self.tts_engine:
            try: self.tts_engine.stop(); self.tts_busy = False
            except: pass

    def on_sim_change(self, key, val, lbl):
        v = float(val); lbl.config(text=f"{v:.2f}")
        self.sim_data[key] = v
        requests.post(f"{self.api_base}/simulate", json=self.sim_data)
        self.update_predictor()

    def update_dashboard(self, telemetry, market):
        for k, v in telemetry.items():
            if k in self.cards: self.cards[k].config(text=str(v))
        
        # V15.0 Live Status Indicator
        source = telemetry.get("data_source", "SIMULATED")
        status_text = f"⚙️ SYSTEM: {'STABLE (LIVE DATA)' if source == 'LIVE' else 'STABLE (SIMULATED)'}"
        status_color = self.colors["green"] if source == "LIVE" else self.colors["gold"]
        self.status_lbl.config(text=status_text, fg=status_color)
        
        self.update_predictor()

    def update_predictor(self):
        def _task():
            try:
                res = requests.post(f"{self.api_base}/predict-crop", json=self.sim_data, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    self.after(0, self.draw_predictor, data['scores'], data['recommendation'])
                    self.after(0, lambda: self.cards['suitability'].config(text=f"{data['suitability']}%"))
            except: pass
        threading.Thread(target=_task, daemon=True).start()

    def draw_predictor(self, scores, best):
        self.ax.clear(); self.ax.set_facecolor("#0c1117")
        crops = list(scores.keys()); vals = list(scores.values())
        colors = ['#00d1ff' if c != best else '#00f07f' for c in crops]
        self.ax.barh(crops, vals, color=colors)
        self.ax.set_xlim(0, 100); self.ax.tick_params(colors="white", labelsize=8)
        self.canvas.draw()

    def speak(self, text, summary_localized=None):
        if not self.voice_active or not self.tts_engine: return
        def _tts():
            if self.tts_busy: return
            self.tts_busy = True
            try:
                voices = self.tts_engine.getProperty('voices')
                target_lang = self.voice_lang_var.get().lower()
                
                # V17.0: Enhanced Voice Search for Indian Languages
                voice_id = None
                for v in voices:
                    v_name = v.name.lower()
                    v_lang = v.languages[0].lower() if hasattr(v, 'languages') and v.languages else ""
                    
                    if target_lang in v_name or target_lang[:2] in v_lang:
                        voice_id = v.id
                        break
                
                if voice_id:
                    self.tts_engine.setProperty('voice', voice_id)
                
                # Priority: Localized Summary > Full Text (Cleaned)
                speech_text = summary_localized if summary_localized else text
                
                clean_text = str(speech_text).replace("**", "").replace("__", "").replace("#", "").replace("*", "")
                self.tts_engine.say(clean_text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
            finally: 
                self.tts_busy = False
        threading.Thread(target=_tts, daemon=True).start()

    def analyze_geographic_intelligence(self):
        """V16.0: Scientific Realism with Real-Time Entry Sync"""
        # Sync Entry & Combo data before request
        for k, v in self.geo_entries.items():
            self.sim_data[k] = v.get().strip()
        self.sim_data["soil_type"] = self.soil_var.get()
        self.sim_data["season"] = self.season_var.get()

        self.display_chat("SYS", f"Establishing Scientific Web Uplink for {self.sim_data['place']}...")
        def _task():
            try:
                # Add small variance (0.95-1.05) for realistic data drift
                self.sim_data["variance"] = random.uniform(0.95, 1.05)
                res = requests.post(f"{self.api_base}/geographic-intelligence", json=self.sim_data, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    self.after(0, lambda: self.display_chat("GEO-INTEL", data['intelligence']))
                    self.after(0, self.draw_predictor, data['scores'], data['best_crop'])
                    self.after(0, lambda: self.speak(data['intelligence'], data.get('speech_summary')))
                    # Sync dashboard sensors too
                    self.after(0, self.bootstrap_once)
                else:
                    self.after(0, lambda: self.display_chat("SYS", "Geo-Link Failed."))
            except Exception as e:
                self.after(0, lambda: self.display_chat("ERROR", f"Geographic analysis failed: {str(e)}"))
        threading.Thread(target=_task, daemon=True).start()

    def bootstrap_once(self):
        """Force a single dashboard sensor update for the new location"""
        try:
            res = requests.get(f"{self.api_base}/live-data", timeout=3)
            if res.status_code == 200:
                all_data = res.json()
                self.update_dashboard(all_data['telemetry'], all_data['market'])
        except: pass

    def clear_chat_history(self):
        """V14.0: Clear chat history"""
        self.chat_history = []
        self.chat_out.config(state="normal")
        self.chat_out.delete(1.0, "end")
        self.chat_out.config(state="disabled")
        self.display_chat("SYS", "Chat history cleared. Ready for new session.")

    def upload_and_diagnose(self, re_trigger=False):
        if not re_trigger:
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
            if not file_path: return
            with open(file_path, "rb") as f: self.last_img_base64 = base64.b64encode(f.read()).decode('utf-8')
            img = Image.open(file_path).resize((180, 100), Image.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(img)
            self.after(0, lambda: self.vision_preview.config(image=self.img_tk, text=""))
        
        self.display_chat("SYS", f"Regional Bio-Scan Initiated... ({self.lang_var.get()})")
        def _task():
            try:
                res = requests.post(f"{self.api_base}/vision-diagnosis", json={
                    "image_base64": self.last_img_base64, "language": self.lang_var.get()
                }, timeout=45)
                data = res.json(); ans = data.get("answer", "Faulty Connection.")
                self.last_ai_briefing = ans; self.last_condition_label = ans.split('.')[0] if '.' in ans else "Active Bio-Risk"
                self.after(0, self.display_chat, "BIO-SCAN", ans)
                self.after(0, lambda: self.speak(ans, data.get("speech_summary")))
            except Exception as e: self.after(0, self.display_chat, "ERROR", f"Bio-Scan Fault: {str(e)}")
        threading.Thread(target=_task, daemon=True).start()


    def send_ai_query(self):
        msg = self.chat_in.get()
        if not msg:
            return
        self.chat_in.delete(0, tk.END)
        self.display_chat("OPERATOR", msg)
        self.chat_history.append({"role": "user", "content": msg})
        def _task():
            try:
                res = requests.post(f"{self.api_base}/chat", json={
                    "message": msg, "context_data": {**self.sim_data, "history": self.chat_history}, 
                    "language": self.lang_var.get()
                })
                data = res.json()
                ans = data.get("answer", "Link lost.")
                self.chat_history.append({"role": "assistant", "content": ans})
                self.last_ai_briefing = ans
                self.after(0, lambda: self.display_chat("STRATEGIST", ans))
                self.after(0, lambda: self.speak(ans, data.get("speech_summary")))
            except Exception as e:
                self.after(0, lambda: self.display_chat("ERROR", str(e)))
        threading.Thread(target=_task, daemon=True).start()

    def display_chat(self, sender, text):
        self.chat_out.config(state="normal")
        color = self.colors["accent"]
        if sender == "OPERATOR": color = "white"
        elif sender == "SYS": color = self.colors["gold"]
        elif sender == "BIO-SCAN": color = self.colors["green"]
        
        self.chat_out.insert("end", f"\n[{sender}] ", "bold")
        self.chat_out.tag_configure("bold", font=("Inter", 9, "bold"), foreground=color)
        
        # V15.0 Rapid Typing Effect
        def _type(i=0):
            if i < len(text):
                self.chat_out.config(state="normal")
                self.chat_out.insert("end", text[i])
                self.chat_out.config(state="disabled")
                self.chat_out.see("end")
                # Speed control: 5ms per char for "High Accuracy/Speed" feel
                self.after(5, lambda: _type(i+1))
            else:
                self.chat_out.config(state="normal")
                self.chat_out.insert("end", "\n")
                self.chat_out.config(state="disabled")
                self.chat_out.see("end")
        
        _type()

    def open_analytics_window(self):
        win = tk.Toplevel(self); win.title("🧬 REGIONAL ANALYTICS"); win.geometry("800x500"); win.configure(bg="#05070a")
        f = plt.Figure(figsize=(6, 4)); f.patch.set_facecolor('#05070a'); ax = f.add_subplot(111); ax.set_facecolor('#0c1117')
        ax.plot([random.uniform(2, 8) for _ in range(50)], color=self.colors["accent"])
        ax.axis('off'); canvas = FigureCanvasTkAgg(f, master=win); canvas.get_tk_widget().pack(fill="both", expand=True); canvas.draw()

    def generate_report(self):
        try:
            if self.last_ai_briefing: self.speak(self.last_ai_briefing)
            payload = {
                "data": self.sim_data, "recommendation": self.last_ai_briefing, 
                "sector": self.sector_var.get(), "history": self.chat_history,
                "image_base64": self.last_img_base64, "condition_name": self.last_condition_label,
                "language": self.lang_var.get(),
                "country": self.sim_data["country"], "state": self.sim_data["state"],
                "place": self.sim_data["place"], "soil_type": self.sim_data["soil_type"]
            }
            res = requests.post(f"{self.api_base}/generate-report", json=payload)
            if res.status_code == 200: webbrowser.open(res.json()['report_url'])
            else: messagebox.showerror("Engine Fault", f"V13.5 Safety Triggered: {res.json().get('message')}")
        except Exception as e: messagebox.showerror("Error", f"Report failed: {str(e)}")

if __name__ == "__main__":
    app = UltimateAgriCommandV14(); app.mainloop()
