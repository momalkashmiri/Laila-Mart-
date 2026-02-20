# 🔧 Troubleshooting Guide

## Login Issues

### "Invalid credentials"
- Check your `secrets.toml` — the `[auth]` section must have `admin_user` and `admin_password`
- On Streamlit Cloud, verify secrets are saved in the dashboard under **Settings → Secrets**

---

## File Upload Issues

### "Missing required columns: Barcode, Sale Price, Stock"
- Open your stock report and confirm the exact column names
- Column names are case-sensitive. They must be exactly: `Barcode`, `Sale Price`, `Stock`
- Remove any leading/trailing spaces in column headers

### "Unsupported file type"
- Only `.xls`, `.xlsx`, and `.csv` files are supported
- If your file is `.xlsm`, save it as `.xlsx` first

### ".xls file fails to read"
- Ensure `xlrd>=2.0.1` is in `requirements.txt`
- Old `.xls` files (Excel 97-2003) require the `xlrd` engine

---

## Template File Issues

### "Template file (Laila_Mart_is6o.csv) not found"
- Confirm `Laila_Mart_is6o.csv` is in the same directory as `app.py`
- On Streamlit Cloud, this file must be committed to your GitHub repository
- The file is loaded from multiple fallback paths; check the console logs

---

## SFTP Upload Issues

### "Authentication failed"
- Double-check the `username` and `password` in secrets
- The password may contain special characters — ensure the entire value is in quotes in `secrets.toml`

### "Connection timeout"
- Verify the `host` is reachable from Streamlit Cloud's network
- Port 22 must be open on the server's firewall
- Test connectivity: `ssh username@host -p 22` from a local terminal

### "Permission denied"
- The SFTP user may not have write access to the `catalog` directory
- Contact your server administrator to grant write permissions

### "Directory doesn't exist"
- The `sftp_helper.py` script automatically creates the `catalog` directory
- If it still fails, the parent directories may not be accessible
- Manually create the path on the server: `/home/YOUR_USERNAME/catalog`

### "paramiko not installed"
- Ensure `paramiko>=3.4.0` is in `requirements.txt`
- Redeploy the app after adding it

---

## Processing Issues

### Barcodes appear as text instead of numbers
- The app converts all barcodes to integers using `pd.to_numeric`
- Barcodes that can't be converted (e.g., contain letters) are dropped from matching
- Check the "Matched" vs "Total" count in the summary

### Active column is all 0s
- Verify the `Stock` column in your input contains numeric values
- Items are marked active (1) only when quantity > 3

---

## General Debugging

1. Check Streamlit Cloud logs: Dashboard → **"Manage app" → Logs**
2. Run locally first: `streamlit run app.py`
3. Add a test with minimal data (3 rows) to isolate the issue
