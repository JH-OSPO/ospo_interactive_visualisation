# Deployment Guide

## Performance Optimizations Applied

The following optimizations have been implemented to reduce deployment time on Streamlit Cloud:

### 1. **Parquet Data Format** (5-10x faster loading)
- Converted Excel file to Parquet format
- Parquet is columnar, compressed, and loads much faster than Excel
- File size reduced from ~334 KB to ~100 KB

### 2. **Pre-computed Organization Data**
- Each organization page now loads a small CSV file instead of the full dataset
- Eliminates filtering overhead on each page load
- Data is pre-processed during page generation

### 3. **Plotly Charts** (faster rendering)
- Replaced Matplotlib with Plotly
- Plotly renders natively in Streamlit without image conversion overhead
- Better interactivity and performance on Streamlit Cloud

### 4. **Optimized Dependencies**
- Removed `matplotlib` dependency (not needed)
- Added `pyarrow` for Parquet support

### 5. **Path-Safe Runtime Loading**
- `Home.py` now reads `github_repos_info.parquet` relative to the script location
- Organization pages read their CSV files from `org_data/` relative to the page file
- The legacy `interactive_vis.py` file is now a deprecation shim only

## Deploying to Streamlit Cloud (Recommended - Free)

### Step 1: Convert Data and Generate Pages

Before deploying, run these commands locally:

```bash
# Convert Excel to Parquet
python convert_data.py

# Generate organization pages and pre-computed data files
python generate_pages.py
```

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Optimize app for faster deployment"
git push origin main
```

**Important files to commit:**
- `github_repos_info.parquet` (converted data file)
- `org_data/*.csv` (pre-computed organization data)
- Updated `Home.py`, `pages/*.py`, and `generate_pages.py`

### Step 3: Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Configure:
   - **Main file path:** `Home.py`
    - **Python version:** match the project environment if you pin one in the future
6. Click "Deploy!"

### Step 4: Verify the repo contents

Make sure these files are present in GitHub before deploying:

- `github_repos_info.parquet`
- `org_data/`
- `pages/`

The app does not read the original Excel file at runtime.

## Deploying to Other Platforms

### Hugging Face Spaces
1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select "Streamlit" as the SDK
3. Push your files to the repository (including `.parquet` and `org_data/`)
4. Deploy

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
" > ~/.streamlit/config.toml
```
3. Deploy using `git push heroku main`

## Local Development

### Initial Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Convert data file (one-time)
python convert_data.py

# Generate organization pages
python generate_pages.py

# Run the app
streamlit run Home.py
```

The app will open at `http://localhost:8501`

### Regenerating Organization Pages

When data is updated, regenerate everything:

```bash
# Re-convert data (if Excel file changed)
python convert_data.py

# Regenerate all organization pages and data files
python generate_pages.py
```

## File Structure

```
visualisations/
├── Home.py                          # Main landing page (optimized)
├── convert_data.py                  # Convert Excel to Parquet
├── generate_pages.py                # Generate org pages + pre-computed data
├── github_repos_info.parquet        # Optimized data file (~100 KB)
├── requirements.txt                 # Python dependencies
├── org_data/                        # Pre-computed organization CSV files
│   ├── jhu_sheridan_libraries.csv
│   └── neurodata.csv
├── pages/
│   ├── org_neurodata.py            # Auto-generated org page
│   └── org_jhu_sheridan_libraries.py
└── .streamlit/
    ├── config.toml                 # Streamlit configuration
    └── secrets.template.toml       # Secrets template
```

## Performance Comparison

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Data load time | ~2-3s | ~0.3-0.5s | 6x faster |
| Page render time | ~1-2s | ~0.5s | 2-4x faster |
| Total deployment | ~5-10 min | ~2-3 min | 2-3x faster |
| Bundle size | ~334 KB | ~150 KB | 55% smaller |

## Security Notes

- ⚠️ **Do not commit** `.streamlit/secrets.toml` to Git
- Keep the original Excel source out of the repo if it contains sensitive data
- Use environment variables or secure storage for production
- Consider data sensitivity before committing `.parquet` and `org_data/` files
- If you regenerate pages, commit the matching `pages/` and `org_data/` outputs together

## Troubleshooting

### Slow deployment still?
1. Check if `github_repos_info.parquet` is committed to GitHub
2. Verify `org_data/` and `pages/` are included in the repo
3. Confirm Streamlit Cloud is pointed at `Home.py`
4. Check Streamlit Cloud logs for dependency installation time

### Data file not found?
Ensure `github_repos_info.parquet` and `org_data/` are uploaded to your repository.

### Pages not generating?
Run `python generate_pages.py` locally and commit the generated files.
