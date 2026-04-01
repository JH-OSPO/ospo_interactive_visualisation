"""
Convert Excel data to Parquet format for faster loading.
Run this script once to convert the data file.
"""
import pandas as pd

print("Converting Excel to Parquet...")
df = pd.read_excel("github_repos_info_20251217_ALL.xlsx")

# Fix data type issues for Parquet compatibility
# Convert object columns that may have mixed types to string
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].fillna('').astype(str)

df.to_parquet("github_repos_info.parquet", index=False)
print(f"✅ Converted {len(df)} rows to github_repos_info.parquet")
print(f"File size will be significantly smaller and loads 5-10x faster")
