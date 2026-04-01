"""
Generate Streamlit pages for each organization with more than 100 repositories.
Run this script whenever the data file is updated.
"""
import os
import pandas as pd

# Load data
df = pd.read_excel("github_repos_info_20251217_ALL.xlsx")

# Get organization counts
org_counts = df.groupby("Organization")["Repository Name"].nunique().reset_index()
org_counts.columns = ["Organization", "repo_count"]

# Filter organizations with more than 100 repos
filtered_orgs = org_counts[org_counts["repo_count"] > 100].sort_values("repo_count", ascending=False)

print(f"Found {len(filtered_orgs)} organizations with more than 100 repositories")

# Create pages directory if it doesn't exist
os.makedirs("pages", exist_ok=True)

# Clear existing org pages
for file in os.listdir("pages"):
    if file.startswith("org_") and file.endswith(".py"):
        os.remove(os.path.join("pages", file))
        print(f"Removed old page: {file}")

# Generate page for each organization
for idx, row in filtered_orgs.iterrows():
    org_name = row["Organization"]
    repo_count = row["repo_count"]
    
    # Create safe filename
    safe_name = org_name.replace(" ", "_").replace("/", "_").replace("-", "_")
    filename = f"pages/org_{safe_name}.py"
    
    # Generate page content
    page_content = f'''import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="{org_name} - OSPO Dashboard", layout="wide", page_icon="📊")

# Navigation link
if st.sidebar.button("← Back to Home"):
    st.switch_page("Home.py")

st.title("📊 {org_name}")
st.markdown(f"**Repository Count:** {repo_count:,}")


@st.cache_data
def load_data():
    return pd.read_excel("github_repos_info_20251217_ALL.xlsx")


df = load_data()
org_df = df[df["Organization"] == "{org_name}"].copy()

# Process binary columns
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

# Compliance Overview
st.subheader("Compliance Overview")

compliance = org_df[binary_cols].mean() * 100
compliance_df = compliance.reset_index()
compliance_df.columns = ["Metric", "Compliance %"]

fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.tab10.colors[: len(compliance_df)]
ax.bar(compliance_df["Metric"], compliance_df["Compliance %"], color=colors)
ax.set_ylabel("Compliance %")
ax.set_title("{org_name} - Compliance Metrics")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Display compliance percentages
col1, col2, col3, col4, col5 = st.columns(5)
metrics = {{
    "README": compliance["has_readme"],
    "License": compliance["has_license"],
    "Citation": compliance["has_citation"],
    "Contributing": compliance["has_contributing"],
    "Tags": compliance["has_tags"],
}}
for i, (metric, value) in enumerate(metrics.items()):
    with [col1, col2, col3, col4, col5][i]:
        st.metric(metric, f"{{value:.1f}}%")

# Repository Details
st.subheader("Repository Details")

display_df = org_df[["Repository Name", "repo_url"] + binary_cols].copy()

editor_key = "repo_editor_{org_name}"

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

for col in binary_cols:
    edited_df[col] = edited_df[col].astype(bool)

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
    file_name="{safe_name}_repositories.csv",
    mime="text/csv",
)
'''
    
    with open(filename, "w") as f:
        f.write(page_content)
    
    print(f"Created: {filename}")

print(f"\n✅ Generated {len(filtered_orgs)} organization pages")
print("Run the Streamlit app with: streamlit run Home.py")
