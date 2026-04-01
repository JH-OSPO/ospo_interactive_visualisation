mkdir -p ~/.streamlit/

echo "[server]
headless = true
port = $PORT
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
" > ~/.streamlit/config.toml
