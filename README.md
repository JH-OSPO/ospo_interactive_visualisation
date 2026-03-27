# OSPO Dashboard

An interactive Streamlit dashboard for visualizing organization compliance with repository best practices.

## Features

- Filter organizations by minimum repository count
- View compliance metrics for licenses, READMEs, citations, contributing guidelines, and tags
- Identify repositories missing best practices
- Explore detailed repository-level data

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```bash
streamlit run interactive_vis.py
```

The dashboard will open in your default browser at `http://localhost:8501`.

## Data

The dashboard expects an Excel file named `github_repos_info_20251217_ALL.xlsx` in the same directory with the following columns:
- `Organization`
- `Repository Name`
- `License`
- `has_readme`
- `has_license`
- `has_citation`
- `has_contributing`
- `has_tags`
- `repo_url`

## Metrics

The dashboard displays compliance percentages for:
- **README**: Repositories with a README file
- **License**: Repositories with a license
- **Citation**: Repositories with citation information
- **Contributing**: Repositories with contributing guidelines
- **Tags**: Repositories with version tags
