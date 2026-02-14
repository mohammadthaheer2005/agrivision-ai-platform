# 🛰️ AgriVision AI Platform
### *The Next Generation of Intelligent Crop Management & Precision Agriculture*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Groq AI](https://img.shields.io/badge/AI-Groq-orange.svg)](https://groq.com/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-success.svg)]()

AgriVision AI is an enterprise-grade, computer vision-powered platform designed to revolutionize modern farming. By merging advanced AI diagnostics with real-time environmental telemetry, we empower agronomists and farmers to make data-driven decisions with clinical precision.

---

## 🚀 Key Capabilities

### 🔍 **Precision Bio-Scan (Computer Vision)**
Leveraging state-of-the-art vision models (LLaVA/Qwen via Groq & HuggingFace), the platform identifies crop diseases, pests, and nutrient deficiencies from a single image. It provides:
*   **Instant Diagnosis**: Specific disease identification with confidence scores.
*   **Scientific Rationale**: Deep-dive into pathogen causes and visual markers.
*   **Treatment Protocols**: ICAR & TNAU-aligned chemical and organic recommendations.

### 🌍 **Geographic Intelligence**
A specialized analytical engine that processes regional data to maximize yield:
*   **Crop Suitability**: Scientifically validated scores for over 20+ commercial crops.
*   **Regional Knowledge**: Integration with localized agricultural databases across India.
*   **Dynamic Intelligence**: Automated Wikipedia-assisted contextual research for any location globally.

### 📊 **Industrial Telemetry & Analytics**
Monitor your field in real-time with an integrated sensor matrix:
*   **Environmental Tracking**: Live monitoring of Temperature, Humidity, Soil pH, and NPK levels.
*   **Market Intelligence**: Real-time commodity price tracking and weather forecasting.
*   **Yield Forecasting**: Predictive analytics for future harvest cycles.

### 📜 **Multi-Language Industrial Reporting**
Generate professional audit reports at the click of a button.
*   **6-Language Support**: English, Tamil, Hindi, Telugu, Urdu, and Malayalam.
*   **Audit-Ready PDFs**: Comprehensive reports including diagnosis, telemetry, and treatment schedules.

---

## 🛠️ Technology Stack

*   **Frontend**: Streamlit (Elite Cyber-Industrial UI)
*   **Backend**: FastAPI (High-performance asynchronous processing)
*   **Core AI Engine**: 
    *   **LLM**: Groq Llama-3.3 (70B) for specialized agricultural reasoning.
    *   **Vision**: Qwen2.5-VL for botanical identification.
*   **Data Sources**: OpenWeatherMap API, Commodities-API, ICAR Knowledge Hub.
*   **PDF Engine**: Custom Report Engine via FPDF2.

---

## 📂 Project Structure

```text
├── 📂 agriculture_ai
│   ├── streamlit_app.py        # Main Dashboard (Frontend)
│   ├── 📂 backend
│   │   ├── main.py             # FastAPI Server Engine
│   │   ├── disease_database.py # Knowledge Base
│   │   ├── report_engine.py    # PDF Generation Logic
│   │   └── .env                # (Excluded) API Keys
│   ├── 📂 frontend
│   │   └── 📂 src/index.css    # Custom Styling
│   ├── requirements.txt
│   └── .gitignore
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
* Python 3.9 or higher
* Git

### 2. Clone and Install
```bash
git clone https://github.com/mohammadthaheer2005/agrivision-ai-platform.git
cd agrivision-ai-platform
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the `backend/` directory:
```env
GROQ_API_KEY=your_key_here
HUGGING_FACE_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
COMMODITIES_API_KEY=your_key_here
```

### 4. Launching the Platform

**Start the Backend Server (Port 8002):**
```bash
cd backend
python main.py
```

**Start the Frontend Dashboard:**
```bash
# From the root directory
streamlit run streamlit_app.py
```

---

## 🛡️ Security & Privacy
*   **Data Protection**: All API keys are managed via environment variables and excluded from version control.
*   **Field Data**: Telemetry data is processed locally and formatted for professional auditing without external data leakage.

---

## 🤝 Contribution
AgriVision AI is built for the community. If you have suggestions for new disease models or regional data integrations:
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

*Developed by **Mohammad Thaheer** - Empowering Agriculture through AI.*
