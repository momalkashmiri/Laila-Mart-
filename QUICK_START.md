# 🚀 QUICK START GUIDE

## What You Have

A complete automated web application for converting stock reports to Laila Mart format!

## Files Included

1. **app.py** - Main Streamlit web application
2. **requirements.txt** - Python dependencies
3. **sftp_helper.py** - SFTP upload functionality
4. **Laila_Mart_is6o.csv** - Template file
5. **README.md** - Complete documentation
6. **DEPLOYMENT.md** - Deployment instructions
7. **This file** - Quick start guide

## Try It NOW (3 Minutes)

### Option 1: Run on Your Computer

```bash
# 1. Install Python (if not installed)
# Download from: https://www.python.org/downloads/

# 2. Open Terminal/Command Prompt and navigate to this folder

# 3. Install dependencies
pip install streamlit pandas openpyxl xlrd paramiko

# 4. Run the app
streamlit run app.py

# 5. App will open in browser automatically!
# If not, go to: http://localhost:8501
```

**Login:**
- Username: `admin`
- Password: `Naqeeb12345@`

### Option 2: Deploy to Cloud (FREE - Best Option!)

#### Using Streamlit Cloud (Easiest):

1. **Create GitHub account** (if you don't have one)
   - Go to: https://github.com/signup

2. **Create new repository**
   - Click "New repository"
   - Name it: `laila-mart-converter`
   - Keep it Private (recommended)

3. **Upload all these files** to your repository
   - Drag and drop all 7 files

4. **Deploy to Streamlit Cloud**
   - Go to: https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Click "Deploy"

5. **Wait 2-3 minutes** and you're done!
   - You'll get a URL like: `https://laila-mart-converter.streamlit.app`
   - Share this URL with your team!

## How to Use

1. **Login** with credentials above
2. **Upload** your daily stock report (.xls, .xlsx, or .csv)
3. **Click** "Process Stock Report"
4. **Download** the converted Laila_Mart_is6o.csv
5. **Optional:** Upload to FTP or email summary

## What It Does

✅ Converts any stock report to Laila Mart format
✅ Matches barcodes automatically
✅ Calculates active status (quantity > 3 = active)
✅ Shows processing statistics
✅ Downloads ready-to-use CSV file
✅ Can upload directly to your FTP server
✅ Sends email summaries

## Features

- 🔐 Secure login
- 📊 Real-time preview
- 📈 Processing statistics
- 💾 One-click download
- 🌐 FTP auto-upload
- 📧 Email notifications
- 📱 Works on mobile

## Your FTP Details (Already Configured)

- **Host:** vendor-automation-sftp-live-ap.prod.aws.qcommerce.live
- **Port:** 22
- **User:** FP_PK_aca38750-f6ba-464a-9316-87415735d1e3
- **Upload Directory:** /vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/catalog
- **Email:** lailavegetableoil1@gmail.com

Files will be automatically uploaded to the **catalog** directory on your server!

## Need Help?

### Common Issues:

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**"Template file not found":**
- Make sure `Laila_Mart_is6o.csv` is in the same folder as `app.py`

**"Port already in use":**
```bash
streamlit run app.py --server.port=8502
```

### Still stuck?

1. Check `README.md` for detailed instructions
2. Check `DEPLOYMENT.md` for deployment options
3. Make sure all files are in the same folder

## Next Steps

After you get it running:

1. ✅ Test with a sample stock report
2. ✅ Verify the output matches your expectations
3. ✅ Test FTP upload (if needed)
4. ✅ Share the URL with your team
5. ✅ Change the default password (see README.md)

## Customization

Want to change something?

- **Login password:** Edit `app.py` line 22-23
- **Email address:** Edit `app.py` line 27
- **Active threshold:** Edit `app.py` line 169 (currently > 3)
- **FTP settings:** Edit `app.py` lines 18-21

## What Makes This Special?

🎯 **No technical knowledge needed** - Just upload and download
⚡ **Lightning fast** - Processes thousands of items in seconds
🔒 **Secure** - Password protected with encrypted FTP
☁️ **Cloud-ready** - Deploy once, use everywhere
📱 **Mobile-friendly** - Works on phones and tablets

## Cost

**FREE!** 
- Streamlit Cloud: Free forever
- Running locally: Free
- No monthly fees, no subscriptions

## Support

Questions? Check the documentation:
- `README.md` - Full documentation
- `DEPLOYMENT.md` - Deployment guide

---

**Ready to automate your stock reports? Start now! 🚀**

Just run: `streamlit run app.py`
