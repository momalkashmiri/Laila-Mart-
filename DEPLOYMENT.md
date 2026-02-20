# 🚀 Deployment Guide — Streamlit Cloud

## Prerequisites

- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

---

## Step 1: Prepare your GitHub Repository

1. Create a new GitHub repository (public or private)
2. Push all files:

```bash
git init
git add .
git commit -m "Initial commit: Laila Mart Stock Processor"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

> ⚠️ **Important:** Do NOT commit `.streamlit/secrets.toml` — it's in `.gitignore`.

---

## Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub account and select your repository
4. Set:
   - **Main file path:** `app.py`
   - **Python version:** 3.11
5. Click **"Deploy!"**

---

## Step 3: Add Secrets in Streamlit Dashboard

1. In your Streamlit Cloud app dashboard, click **"⋮" → Settings → Secrets**
2. Paste the following and fill in your values:

```toml
[ftp]
host = "vendor-automation-sftp-live-ap.prod.aws.qcommerce.live"
port = 22
username = "FP_PK_aca38750-f6ba-464a-9316-87415735d1e3"
password = "zCGKp?{52IRsya$Wxj|!>U"
remote_path = "/vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/catalog"

[auth]
admin_user = "admin"
admin_password = "Naqeeb12345@"

[email]
notification_email = "lailavegetableoil1@gmail.com"
```

3. Click **"Save"** — the app will restart automatically.

---

## Step 4: Update the App

To push updates:

```bash
git add .
git commit -m "Update: describe your change"
git push
```

Streamlit Cloud will automatically redeploy within ~30 seconds.

---

## Verifying the Deployment

1. Visit your app URL (e.g., `https://your-app.streamlit.app`)
2. Log in with your credentials
3. Upload a test stock report
4. Check the upload confirmation details for the correct server path

---

## Free Tier Limits (Streamlit Cloud)

| Resource | Limit |
|----------|-------|
| Apps | 1 public app (free) |
| Memory | 1 GB |
| CPU | Shared |
| Storage | No persistent disk |

The app stores upload history in **session state only** — it resets when the browser tab is closed. This is by design for the free tier.
