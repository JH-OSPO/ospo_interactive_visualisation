import streamlit as st

st.set_page_config(page_title="Legacy OSPO Dashboard", layout="wide", page_icon="📊")

st.title("Legacy dashboard removed")
st.warning(
    "This file is kept only to avoid confusion. Use Home.py as the Streamlit Cloud entry point."
)
st.write("Run the app with: streamlit run Home.py")
st.stop()
