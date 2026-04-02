import plotly.express as px
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="OSPO Dashboard", layout="wide", page_icon="📊")
st.title("📊 OSPO Organization Dashboard")

st.markdown("""
Welcome to the OSPO Compliance Dashboard. This dashboard helps track repository compliance
with best practices across different organizations.
""")


@st.cache_data
def load_data():
    data_path = Path(__file__).with_name("github_repos_info.parquet")
    return pd.read_parquet(data_path)


df = load_data()

# Calculate organization stats
org_counts = df.groupby("Organization")["Repository Name"].nunique().reset_index()
org_counts.columns = ["Organization", "repo_count"]

# Sidebar filters
st.sidebar.header("Filters")
min_repos = st.sidebar.number_input("Minimum repo count", value=100, min_value=0)

# Filter organizations
filtered_orgs = org_counts[org_counts["repo_count"] >= min_repos].sort_values(
    "repo_count", ascending=False
)

# Display summary metrics
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Organizations", len(filtered_orgs))
with col2:
    st.metric("Total Repositories", filtered_orgs["repo_count"].sum())
with col3:
    st.metric("Avg Repos per Org", round(filtered_orgs["repo_count"].mean(), 1))

# Organizations table
st.subheader(f"Organizations with ≥{min_repos} Repositories")

if len(filtered_orgs) > 0:
    # Calculate compliance overview for each org
    org_compliance_data = []
    for org in filtered_orgs["Organization"]:
        org_df = df[df["Organization"] == org].copy()
        org_df["has_license"] = org_df["License"].notna() & (org_df["License"] != "")
        binary_cols = ["has_readme", "has_license", "has_citation", "has_contributing", "has_tags"]
        for col in binary_cols:
            if col != "has_license":
                org_df[col] = org_df[col].astype(str).str.lower().isin(["1", "true", "yes"])
        avg_compliance = org_df[binary_cols].mean().mean() * 100
        org_compliance_data.append(
            {"Organization": org, "Repositories": org_df.shape[0], "Avg Compliance %": round(avg_compliance, 1)}
        )

    org_summary_df = pd.DataFrame(org_compliance_data)
    org_summary_df = org_summary_df.merge(filtered_orgs, on="Organization")
    org_summary_df = org_summary_df.sort_values("repo_count", ascending=False)

    st.dataframe(
        org_summary_df[["Organization", "repo_count", "Avg Compliance %"]],
        use_container_width=True,
        hide_index=True,
    )

    # Top 5 organizations chart
    st.subheader("Top 5 Organizations by Repository Count")
    top5 = filtered_orgs.nlargest(5, "repo_count")

    fig = px.bar(
        top5,
        x="repo_count",
        y="Organization",
        orientation="h",
        title="Top 5 Organizations",
        labels={"repo_count": "Number of Repositories", "Organization": ""},
        color="repo_count",
        color_continuous_scale="Blues",
    )
    fig.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ---
    ### Navigation
    Use the sidebar to navigate to individual organization pages or select from the list above.
    Each organization page provides detailed compliance metrics and repository-level data.
    """)
else:
    st.warning(f"No organizations found with ≥{min_repos} repositories. Try lowering the filter.")
