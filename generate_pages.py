"""
Generate Streamlit pages for each organization with more than 100 repositories.
Also creates pre-computed CSV files for each organization to speed up page loading.
Run this script whenever the data file is updated.
"""
import os
import pandas as pd

# Load data
print("Loading data...")
df = pd.read_parquet("github_repos_info.parquet")

# Get organization counts
org_counts = df.groupby("Organization")["Repository Name"].nunique().reset_index()
org_counts.columns = ["Organization", "repo_count"]

# Filter organizations with more than 100 repos
filtered_orgs = org_counts[org_counts["repo_count"] > 100].sort_values(
    "repo_count", ascending=False
)

print(f"Found {len(filtered_orgs)} organizations with more than 100 repositories")

# Create directories
os.makedirs("pages", exist_ok=True)
os.makedirs("org_data", exist_ok=True)

# Clear existing org pages
for file in os.listdir("pages"):
    if file.startswith("org_") and file.endswith(".py"):
        os.remove(os.path.join("pages", file))
        print(f"Removed old page: {file}")

# Clear existing org data files
for file in os.listdir("org_data"):
    if file.endswith(".csv"):
        os.remove(os.path.join("org_data", file))

# Generate page for each organization
for idx, row in filtered_orgs.iterrows():
    org_name = row["Organization"]
    repo_count = row["repo_count"]

    # Create safe filename
    safe_name = org_name.replace(" ", "_").replace("/", "_").replace("-", "_")
    filename = f"pages/org_{safe_name}.py"
    data_filename = f"org_data/{safe_name}.csv"

    # Pre-compute and save organization data
    org_df = df[df["Organization"] == org_name].copy()
    org_df["has_license"] = org_df["License"].notna() & (org_df["License"] != "")
    binary_cols = [
        "has_readme",
        "has_license",
        "has_citation",
        "has_contributing",
        "has_tags",
    ]
    for col in binary_cols:
        if col != "has_license":
            org_df[col] = org_df[col].astype(str).str.lower().isin(["1", "true", "yes"])
        org_df[col] = org_df[col].astype(bool)

    # Save pre-processed data
    org_df.to_csv(data_filename, index=False)
    print(f"Created data file: {data_filename}")

    # Calculate compliance percentages
    compliance = org_df[binary_cols].mean() * 100
    compliance_dict = {
        "README": round(compliance["has_readme"], 1),
        "License": round(compliance["has_license"], 1),
        "Citation": round(compliance["has_citation"], 1),
        "Contributing": round(compliance["has_contributing"], 1),
        "Tags": round(compliance["has_tags"], 1),
    }

    # Generate page content
    page_content = f'''import plotly.express as px
import pandas as pd
import streamlit as st

st.set_page_config(page_title="{org_name} - OSPO Dashboard", layout="wide", page_icon="📊")

# Navigation link
if st.sidebar.button("← Back to Home"):
    st.switch_page("Home.py")

st.title("📊 {{org_name}}")
st.markdown(f"**Repository Count:** {{repo_count:,}}")


@st.cache_data
def load_org_data():
    return pd.read_csv("{data_filename}")


df = load_org_data()
org_name = "{org_name}"
repo_count = {repo_count}

# Compliance Overview
st.subheader("Compliance Overview")

compliance_data = {{
    "Metric": ["README", "License", "Citation", "Contributing", "Tags"],
    "Compliance %": [{compliance_dict["README"]}, {compliance_dict["License"]}, {compliance_dict["Citation"]}, {compliance_dict["Contributing"]}, {compliance_dict["Tags"]}],
}}

fig = px.bar(
    compliance_data,
    x="Metric",
    y="Compliance %",
    title=f"{{org_name}} - Compliance Metrics",
    labels={{"Metric": "", "Compliance %": "Compliance %"}},
    color="Compliance %",
    color_continuous_scale="Blues",
    ymin=0,
    ymax=100,
)
fig.update_layout(showlegend=False, height=400)
st.plotly_chart(fig, use_container_width=True)

# Display compliance percentages
col1, col2, col3, col4, col5 = st.columns(5)
metrics = compliance_data
for i, metric in enumerate(metrics["Metric"]):
    with [col1, col2, col3, col4, col5][i]:
        st.metric(metric, f"{{metrics['Compliance %'][i]}}%")

# Repository Details
st.subheader("Repository Details")

binary_cols = [
    "has_readme",
    "has_license",
    "has_citation",
    "has_contributing",
    "has_tags",
]

display_df = df[["Repository Name", "repo_url"] + binary_cols].copy()

editor_key = "repo_editor_{{org_name}}"

column_config = {{
    "has_readme": st.column_config.CheckboxColumn("has_readme"),
    "has_license": st.column_config.CheckboxColumn("has_license"),
    "has_citation": st.column_config.CheckboxColumn("has_citation"),
    "has_contributing": st.column_config.CheckboxColumn("has_contributing"),
    "has_tags": st.column_config.CheckboxColumn("has_tags"),
}}

edited_df = st.data_editor(
    display_df,
    column_config=column_config,
    use_container_width=True,
    hide_index=True,
    disabled=["Repository Name", "repo_url"],
    key=editor_key,
)

# Missing Best Practices
st.subheader("Missing Best Practices")

missing = (~edited_df[binary_cols]).sum()
missing_df = missing.reset_index()
missing_df.columns = ["Metric", "Missing Count"]

st.dataframe(missing_df, use_container_width=True, hide_index=True)

# Download button
csv = edited_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Repository Data as CSV",
    data=csv,
    file_name="{{org_name}}_repositories.csv",
    mime="text/csv",
)
'''

    with open(filename, "w") as f:
        f.write(page_content)

    print(f"Created: {filename}")

print(f"\n✅ Generated {len(filtered_orgs)} organization pages")
print(f"✅ Created {len(filtered_orgs)} pre-computed data files in org_data/")
print("\nRun the Streamlit app with: streamlit run Home.py")
