# OSPO Dashboard

An interactive Streamlit dashboard for visualizing organization compliance with repository best practices.

## Features

- 📊 **Multi-page architecture** with individual pages for each organization (>100 repos)
- 🏠 **Home page** with overview of all organizations and summary metrics
- 🔍 **Filter organizations** by minimum repository count
- 📈 **View compliance metrics** for licenses, READMEs, citations, contributing guidelines, and tags
- 📝 **Edit data** directly in the dashboard with checkbox controls
- ⬇️ **Download** repository data as CSV
- 🚀 **Ready for deployment** on Streamlit Cloud, Heroku, Railway, and Hugging Face Spaces

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run Home.py
```

The dashboard will open in your default browser at `http://localhost:8501`.

## Project Structure

```
visualisations/
├── Home.py                          # Main landing page with all organizations
├── interactive_vis.py               # Original single-page app (legacy)
├── generate_pages.py                # Script to generate org pages
├── github_repos_info_20251217_ALL.xlsx  # Data file
├── requirements.txt                 # Python dependencies
├── Procfile                         # For Heroku/Railway deployment
├── setup.sh                         # Setup script for deployment
├── DEPLOYMENT.md                    # Detailed deployment instructions
├── pages/
│   ├── org_neurodata.py            # Auto-generated org page
│   └── org_jhu_sheridan_libraries.py
└── .streamlit/
    ├── config.toml                 # Streamlit configuration
    └── secrets.template.toml       # Secrets template
```

## Usage

### Home Page
- View summary metrics for all organizations
- Filter by minimum repository count
- See top 5 organizations by repository count
- Navigate to individual organization pages via sidebar

### Organization Pages
Each organization page includes:
- **Compliance Overview**: Visual chart of compliance metrics
- **Quick Metrics**: 5-column display of compliance percentages
- **Repository Details**: Editable table with checkbox controls
- **Missing Best Practices**: Count of repositories missing each metric
- **Download**: Export repository data as CSV

### Regenerating Pages

When your data file is updated, regenerate organization pages:

```bash
python generate_pages.py
```

This creates individual pages for all organizations with >100 repositories.

## Data Requirements

The dashboard expects an Excel file named `github_repos_info_20251217_ALL.xlsx` with:

| Column | Description |
|--------|-------------|
| `Organization` | Organization name |
| `Repository Name` | Repository name |
| `License` | License name (empty if none) |
| `has_readme` | 1/0 or true/false |
| `has_citation` | 1/0 or true/false |
| `has_contributing` | 1/0 or true/false |
| `has_tags` | 1/0 or true/false |
| `repo_url` | Full repository URL |

## Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Create new app with:
   - **Main file path:** `Home.py`
   - **Python version:** 3.10+
4. Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on other platforms.

## Metrics

The dashboard displays compliance percentages for:
- **README**: Repositories with a README file
- **License**: Repositories with a license
- **Citation**: Repositories with citation information
- **Contributing**: Repositories with contributing guidelines
- **Tags**: Repositories with version tags

## Development

### Local Testing

```bash
streamlit run Home.py
```

### Adding Custom Pages

Create new pages in the `pages/` directory:

```python
# pages/custom_page.py
import streamlit as st

st.set_page_config(page_title="Custom Page", layout="wide")
st.title("My Custom Page")
```

Streamlit automatically detects and adds them to the navigation.

## License

See [LICENSE](LICENSE) file.
