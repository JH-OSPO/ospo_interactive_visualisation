import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="jhu-sheridan-libraries - OSPO Dashboard", layout="wide", page_icon="📊")

# Navigation link
if st.sidebar.button("← Back to Home"):
    st.switch_page("Home.py")

st.title("📊 jhu-sheridan-libraries")
st.markdown(f"**Repository Count:** 117")


@st.cache_data
def load_data():
    return pd.read_excel("github_repos_info_20251217_ALL.xlsx")


df = load_data()
org_df = df[df["Organization"] == "jhu-sheridan-libraries"].copy()

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
ax.set_title("jhu-sheridan-libraries - Compliance Metrics")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Display compliance percentages
col1, col2, col3, col4, col5 = st.columns(5)
metrics = {
    "README": compliance["has_readme"],
    "License": compliance["has_license"],
    "Citation": compliance["has_citation"],
    "Contributing": compliance["has_contributing"],
    "Tags": compliance["has_tags"],
}
for i, (metric, value) in enumerate(metrics.items()):
    with [col1, col2, col3, col4, col5][i]:
        st.metric(metric, f"{value:.1f}%")

# Repository Details
st.subheader("Repository Details")

display_df = org_df[["Repository Name", "repo_url"] + binary_cols].copy()

editor_key = "repo_editor_jhu-sheridan-libraries"

column_config = {
    "has_readme": st.column_config.CheckboxColumn("has_readme"),
    "has_license": st.column_config.CheckboxColumn("has_license"),
    "has_citation": st.column_config.CheckboxColumn("has_citation"),
    "has_contributing": st.column_config.CheckboxColumn("has_contributing"),
    "has_tags": st.column_config.CheckboxColumn("has_tags"),
}

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
    file_name="jhu_sheridan_libraries_repositories.csv",
    mime="text/csv",
)
