import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="OSPO Dashboard", layout="wide")
st.title("Organization Compliance Dashboard")


@st.cache_data
def load_data():
    return pd.read_excel("github_repos_info_20251217_ALL.xlsx")


df = load_data()

org_counts = df.groupby("Organization")["Repository Name"].nunique().reset_index()

org_counts.columns = ["Organization", "repo_count"]

st.sidebar.header("Filters")
min_repos = st.sidebar.number_input("Minimum repo count", value=100)

filtered_orgs = org_counts[org_counts["repo_count"] >= min_repos]

selected_org = st.sidebar.selectbox(
    "Select Organization", filtered_orgs["Organization"]
)

org_df = df[df["Organization"] == selected_org].copy()

st.subheader(selected_org)

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

st.subheader("Compliance Overview")

compliance = org_df[binary_cols].mean() * 100
compliance_df = compliance.reset_index()
compliance_df.columns = ["Metric", "Compliance %"]

fig, ax = plt.subplots()
colors = plt.cm.tab10.colors[: len(compliance_df)]
ax.bar(compliance_df["Metric"], compliance_df["Compliance %"], color=colors)
ax.set_ylabel("Compliance %")
ax.set_title(f"{selected_org} Compliance")
plt.xticks(rotation=45)

st.pyplot(fig)

st.subheader("Repository Details")

display_df = org_df[["Repository Name", "repo_url"] + binary_cols].copy()

editor_key = f"repo_editor_{selected_org}"

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

st.subheader("Missing Best Practices")

missing = (~edited_df[binary_cols]).sum()
missing_df = missing.reset_index()
missing_df.columns = ["Metric", "Missing Count"]

st.dataframe(missing_df, use_container_width=True)
