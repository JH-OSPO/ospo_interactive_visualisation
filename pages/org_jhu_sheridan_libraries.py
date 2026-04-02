import plotly.express as px
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="jhu-sheridan-libraries - OSPO Dashboard", layout="wide", page_icon="📊")

# Navigation link
if st.sidebar.button("← Back to Home"):
    st.switch_page("Home.py")

org_name = "jhu-sheridan-libraries"
repo_count = 117

st.title(f"📊 {org_name}")
st.markdown(f"**Repository Count:** {repo_count:,}")


@st.cache_data
def load_org_data():
    data_path = Path(__file__).resolve().parents[1] / "org_data" / "jhu_sheridan_libraries.csv"
    return pd.read_csv(data_path)


df = load_org_data()

# Compliance Overview
st.subheader("Compliance Overview")

compliance_data = {
    "Metric": ["README", "License", "Citation", "Contributing", "Tags"],
    "Compliance %": [82.1, 100.0, 0.0, 5.1, 21.4],
}

fig = px.bar(
    compliance_data,
    x="Metric",
    y="Compliance %",
    title=f"{org_name} - Compliance Metrics",
    labels={"Metric": "", "Compliance %": "Compliance %"},
    color="Compliance %",
    color_continuous_scale="Blues",
)
fig.update_layout(showlegend=False, height=400)
st.plotly_chart(fig, use_container_width=True)

# Display compliance percentages
col1, col2, col3, col4, col5 = st.columns(5)
metrics = compliance_data
for i, metric in enumerate(metrics["Metric"]):
    with [col1, col2, col3, col4, col5][i]:
        st.metric(metric, f"{metrics['Compliance %'][i]}%")

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

editor_key = f"repo_editor_{org_name}"

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
    file_name=f"{org_name}_repositories.csv",
    mime="text/csv",
)
