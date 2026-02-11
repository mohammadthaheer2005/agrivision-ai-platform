# Agri-Command Industrial V20.0

An advanced AI-powered Agricultural Command Center for industrial auditing, disease diagnosis, and geographic intelligence.

## Features
- **Visual Biological Diagnosis**: Real-time bio-scan of crops for disease detection (using Groq Vision).
- **Geographic Intelligence**: Localized crop suitability analysis and market snapshots.
- **Industrial Multi-Language Reporting**: Automated PDF generation in English, Tamil, Hindi, Telugu, Urdu, and Malayalam.
- **Field Telemetry**: Real-time simulation of soil and environmental metrics (NPK, pH, Temperature, Humidity).
- **Tactical Irrigation & Water Audit**: Intelligent watering and fertigation recommendations.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI Models**: Groq Cloud (LLM & Vision)
- **Reporting**: FPDF2
- **Data**: OpenWeatherMap API & Commodity APIs

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd agriculture_ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory (or use Streamlit Secrets for cloud hosting):
   ```env
   GROQ_API_KEY=your_key_here
   OPENWEATHER_API_KEY=your_key_here
   ```

4. Run the components:

   **Backend:**
   ```bash
   cd backend
   python main.py
   ```

   **Frontend:**
   ```bash
   streamlit run streamlit_app.py
   ```

## Hosting on Streamlit Cloud
1. Push this code to GitHub.
2. Connect your GitHub repo to Streamlit Cloud.
3. In the Streamlit Cloud settings, add your keys to the "Secrets" section.

## License
Industrial Proprietary - Under Agri-Command Protocols.
