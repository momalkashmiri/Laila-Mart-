# Troubleshooting Guide

## Python Version Error (pandas compatibility)

**Error:** `pandas==2.1.4` fails to build on Python 3.13

**Solution:** We've updated the requirements to use compatible versions.

### Files Updated:
1. ✅ **requirements.txt** - Updated to use flexible versions
2. ✅ **.python-version** - Specifies Python 3.11
3. ✅ **runtime.txt** - Backup Python version specification

### For Streamlit Cloud:

**After uploading to GitHub:**

1. **Delete the old app** (if already deployed with errors)
2. **Redeploy** with the new files
3. **Or** in App Settings → Advanced Settings:
   - Set Python version to `3.11`

### Current Requirements (Updated):
```
streamlit>=1.31.0
pandas>=2.2.0
openpyxl>=3.1.2
xlrd>=2.0.1
paramiko>=3.4.0
```

---

## Common Deployment Errors

### 1. Module Not Found

**Error:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
- Ensure all files are uploaded to GitHub
- Check `requirements.txt` is present
- Redeploy the app

### 2. Template File Not Found

**Error:** `FileNotFoundError: Laila_Mart_is6o.csv`

**Solution:**
Update `app.py` line with template file:

```python
# Change this line (around line 245):
template_path = "/mnt/user-data/uploads/Laila_Mart_is6o.csv"

# To this:
template_path = "Laila_Mart_is6o.csv"
```

Make sure `Laila_Mart_is6o.csv` is in your GitHub repository.

### 3. SFTP Connection Failed

**Error:** `Authentication failed` or `Connection timeout`

**Solution:**
- Verify SFTP credentials are correct
- Check network connectivity
- Test with `test_sftp.py` script locally first

### 4. App Crashes on Startup

**Solution:**
1. Check logs in Streamlit Cloud dashboard
2. Verify all files are uploaded
3. Check Python version is 3.11
4. Try restarting the app

---

## Step-by-Step Fix for Current Error

### Option 1: Quick Fix (Recommended)

1. **In your GitHub repository, replace these files:**
   - `requirements.txt` (with updated version)
   - `.python-version` (new file)
   - `runtime.txt` (new file)

2. **Streamlit Cloud will auto-redeploy**
   - Wait 2-3 minutes
   - Check logs for success

### Option 2: Force Python 3.11

In Streamlit Cloud:
1. Go to App Settings
2. Advanced Settings
3. Set Python version: `3.11`
4. Save and Reboot

### Option 3: Local Testing First

```bash
# Use Python 3.11 locally
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test the app
streamlit run app.py
```

If it works locally, deploy to Streamlit Cloud.

---

## Verification Checklist

Before deploying, ensure:

- ✅ All files uploaded to GitHub
- ✅ `requirements.txt` uses `>=` instead of `==`
- ✅ `.python-version` file exists (contains `3.11`)
- ✅ `Laila_Mart_is6o.csv` is in repository
- ✅ No sensitive data committed (use secrets for credentials)

---

## Files Required in GitHub Repository

```
laila-mart-converter/
├── app.py
├── sftp_helper.py
├── requirements.txt
├── Laila_Mart_is6o.csv
├── .python-version
├── runtime.txt
├── .gitignore
├── README.md
├── DEPLOYMENT.md
├── QUICK_START.md
└── test_sftp.py (optional)
```

---

## Testing Locally Before Deployment

```bash
# 1. Install Python 3.11
# Download from: https://www.python.org/downloads/

# 2. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test SFTP (optional)
python test_sftp.py

# 5. Run the app
streamlit run app.py

# 6. Test in browser at http://localhost:8501
```

---

## Still Having Issues?

### Check Streamlit Cloud Logs

1. Go to your app dashboard
2. Click "Manage app"
3. View "Logs" tab
4. Look for specific error messages

### Common Log Messages:

**"Failed to download pandas"**
→ Python version issue (use 3.11)

**"FileNotFoundError"**
→ Missing file in repository

**"ModuleNotFoundError"**
→ Missing dependency in requirements.txt

**"Authentication failed"**
→ Wrong SFTP credentials

---

## Alternative: Use Docker

If Streamlit Cloud continues to have issues:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Deploy to:
- Railway.app (free tier)
- Render.com (free tier)
- Google Cloud Run
- AWS ECS

---

## Need More Help?

1. **Check logs** for specific error messages
2. **Test locally** first with Python 3.11
3. **Verify all files** are in GitHub
4. **Double-check** requirements.txt has flexible versions

The app should work fine once Python 3.11 is used!
