mkdir -p ~/.streamlit/

echo "[server]
headless = true
port = $PORT
enableXsrfProtection = true

[browser]
gatherUsageStats = false
" > ~/.streamlit/config.toml
