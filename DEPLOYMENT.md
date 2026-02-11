# Streamlit Cloud Configuration

This application is ready for deployment on Streamlit Cloud.

## Setup Instructions

1. **Fork/Clone this repository** to your GitHub account.

2. **Go to [Streamlit Cloud](https://share.streamlit.io/)** and sign in with GitHub.

3. **Deploy the app**:
   - Click "New app"
   - Select your repository
   - Set the main file path to: `streamlit_app.py`
   - Click "Deploy"

4. **Configure Secrets**:
   - In your Streamlit Cloud dashboard, go to "Settings" → "Secrets"
   - Add the following secrets:
   
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   OPENWEATHER_API_KEY = "your_openweather_key_here"
   ```

5. **Backend Configuration**:
   - The backend (`backend/main.py`) needs to run separately
   - For production, deploy the FastAPI backend to a service like:
     - Render.com
     - Railway.app
     - Heroku
     - AWS/GCP/Azure
   
   - Update the `API_BASE` variable in `streamlit_app.py` (line 172) to point to your deployed backend URL

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

3. Add your API keys to `.env`

4. Run the backend:
   ```bash
   cd backend
   python main.py
   ```

5. In a new terminal, run the frontend:
   ```bash
   streamlit run streamlit_app.py
   ```

## Notes
- The backend runs on port 8002 by default
- The frontend runs on port 8501 by default
- For Streamlit Cloud deployment, you'll need to host the backend separately
