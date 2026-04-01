# Deployment Guide

## Deploying to Streamlit Cloud (Recommended - Free)

### Step 1: Push to GitHub
Ensure your code is pushed to a GitHub repository:

```bash
git add .
git commit -m "Add multi-page OSPO dashboard"
git push origin main
```

### Step 2: Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Configure:
   - **Main file path:** `Home.py`
   - **Python version:** 3.10 or higher
6. Click "Deploy!"

### Step 3: Upload Data File

Since the Excel file contains sensitive data:

1. In Streamlit Cloud dashboard, go to your app
2. Click "Settings" → "Secrets"
3. **Option A:** Upload the Excel file to a cloud storage (Google Drive, Dropbox) and modify the code to load from URL
4. **Option B:** Convert the Excel file to a format accessible via environment variable

### Alternative: Load Data from URL

Modify `Home.py` and `generate_pages.py` to load from a URL:

```python
@st.cache_data
def load_data():
    url = "https://your-domain.com/github_repos_info_20251217_ALL.xlsx"
    return pd.read_excel(url)
```

## Deploying to Other Platforms

### Hugging Face Spaces
1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select "Streamlit" as the SDK
3. Push your files to the repository
4. Upload the Excel file to the repo

### Railway
1. Create account at [railway.app](https://railway.app)
2. Create new project → "Deploy from GitHub repo"
3. Add `Procfile`: `web: streamlit run Home.py --server.port=$PORT --server.address=0.0.0.0`
4. Deploy

### Heroku
1. Create `Procfile`: `web: sh setup.sh && streamlit run Home.py`
2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```
3. Deploy using `git push heroku main`

## Local Development

Run locally with:

```bash
streamlit run Home.py
```

The app will open at `http://localhost:8501`

## Regenerating Organization Pages

When data is updated, regenerate the organization pages:

```bash
python generate_pages.py
```

This will create individual pages for all organizations with >100 repositories.

## File Structure

```
visualisations/
├── Home.py                          # Main landing page
├── interactive_vis.py               # Original single-page app (keep for reference)
├── generate_pages.py                # Script to generate org pages
├── github_repos_info_20251217_ALL.xlsx  # Data file
├── requirements.txt                 # Python dependencies
├── pages/
│   ├── org_neurodata.py            # Auto-generated org page
│   └── org_jhu_sheridan_libraries.py
└── .streamlit/
    ├── config.toml                 # Streamlit configuration
    └── secrets.template.toml       # Secrets template
```

## Security Notes

- ⚠️ **Do not commit** `.streamlit/secrets.toml` to Git
- Add Excel file to `.gitignore` if it contains sensitive data
- Use environment variables or secure storage for production
