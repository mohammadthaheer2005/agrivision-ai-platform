# GitHub Push Instructions

Your repository is ready to push to GitHub! Follow these steps:

## Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. Name it: `agri-command-industrial` (or your preferred name)
4. **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Push Your Code

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/agri-command-industrial.git

# Push the code
git branch -M main
git push -u origin main
```

Or run this single command (replace YOUR_USERNAME):
```bash
cd d:\AI_Agent_Build\dist\AI_Agent_Pro_App\agriculture_ai
git remote add origin https://github.com/YOUR_USERNAME/agri-command-industrial.git
git branch -M main
git push -u origin main
```

## Step 3: Verify Security

After pushing, verify that sensitive files are NOT visible on GitHub:
- ✅ `.env.example` should be visible
- ❌ `.env` or `backend/.env` should NOT be visible
- ❌ `reports/` folder should NOT be visible
- ❌ `*.pdf` files should NOT be visible

## Step 4: Deploy to Streamlit Cloud

1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/agri-command-industrial`
5. Main file path: `streamlit_app.py`
6. Click "Advanced settings" → "Secrets"
7. Add your secrets:
   ```toml
   GROQ_API_KEY = "your_actual_key_here"
   OPENWEATHER_API_KEY = "your_actual_key_here"
   ```
8. Click "Deploy"

## Important Notes

- **Backend Hosting**: The FastAPI backend (`backend/main.py`) needs separate hosting
  - Recommended: Render.com, Railway.app, or Heroku
  - After deploying backend, update `API_BASE` in `streamlit_app.py` line 172
  
- **For Local Testing**: 
  - Copy `.env.example` to `.env` in the backend folder
  - Add your actual API keys
  - Run both backend and frontend locally

## Repository Status
✅ Git initialized
✅ All files committed
✅ Sensitive data protected
✅ Ready to push to GitHub
