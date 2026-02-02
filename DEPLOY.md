# Deploying Your Trading Bot

To generate a public URL for your trading bot, you can deploy it to **Streamlit Community Cloud** directly from GitHub.

## Prerequisites
1. Ensure your code is pushed to GitHub.
2. Ensure `requirements.txt` is present in your repository.

## Steps to Deploy

1. **Sign Up / Login**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Login with your GitHub account.

2. **Create App**
   - Click **"New app"**.
   - Select your GitHub repository (`Trading-Bot-on-Binance-Futures-Testnet`).
   - **Branch**: `main` (or master).
   - **Main file path**: `trading_bot/ui.py`.
   - Click **"Deploy!"**.

3. **Configure Secrets (Crucial!)**
   Your bot needs API keys to work. Do NOT commit them to GitHub.
   - Once the app is deploying, go to **Settings** (three dots in top right) -> **Secrets**.
   - Add your keys in TOML format:
     ```toml
     [general]
     BINANCE_API_KEY = "your_api_key_here"
     BINANCE_API_SECRET = "your_api_secret_here"
     ```
   - Save the secrets.

4. **Reboot App**
   - If the app crashed initially due to missing keys, click **"Reboot"**.

## Public URL
Streamlit will generate a URL like:
`https://trading-bot-futures-testnet.streamlit.app`

You can share this URL to access your bot from anywhere.
