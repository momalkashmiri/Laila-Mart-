# Laila Mart Stock Report Converter

Automated web application for converting daily stock reports to Laila Mart format with FTP upload capability.

## Features

✅ **User Authentication** - Secure login (admin/Naqeeb12345@)
✅ **File Upload** - Support for .xls, .xlsx, .csv files
✅ **Automatic Conversion** - Converts to Laila_Mart_is6o.csv format
✅ **Active Status Formula** - Automatically calculates active = 1 if quantity > 3
✅ **Preview & Statistics** - Shows processing summary before download
✅ **FTP Auto-Upload** - Direct upload to your server
✅ **Email Notifications** - Summary reports to lailavegetableoil1@gmail.com
✅ **Mobile Friendly** - Works on any device

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Login Credentials

- **Username:** admin
- **Password:** Naqeeb12345@

## How to Use

1. **Login** with your credentials
2. **Upload** your daily stock report file
3. **Click** "Process Stock Report" button
4. **Review** the processing summary
5. **Download** the converted file
6. **Optional:** Upload to FTP or send email summary

## File Requirements

Your stock report must contain these columns:
- `Barcode` - Product barcode
- `Sale Price` - Selling price
- `Stock` - Quantity in stock

## Deployment Options

### Option 1: Streamlit Cloud (Free & Easy)

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your GitHub repository
4. Deploy with one click
5. Share the URL with your team

### Option 2: Heroku

1. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT
   ```
2. Deploy to Heroku

### Option 3: Your Own Server

1. Install dependencies
2. Run with: `streamlit run app.py --server.port=8080`
3. Access via your server IP

## FTP/SFTP Configuration

The app is configured for SFTP upload with these details:
- **Host:** sftp://vendor-automation-sftp-live-ap.prod.aws.qcommerce.live
- **Port:** 22
- **Username:** FP_PK_aca38750-f6ba-464a-9316-87415735d1e3
- **Upload Directory:** /vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/catalog

The SFTP upload is fully implemented using the `paramiko` library and will automatically upload the converted file to the catalog directory.

## Email Notifications

Email notifications are configured to send to:
- **Email:** lailavegetableoil1@gmail.com

**Note:** You need to configure an SMTP server to enable actual email sending.

## Security Notes

⚠️ **Important:** 
- Change default admin password after first login
- Keep FTP credentials secure
- Don't commit sensitive credentials to public repositories
- Use environment variables for production deployment

## Customization

### Change Login Credentials

Edit in `app.py`:
```python
ADMIN_USER = "admin"
ADMIN_PASS = "your_new_password"
```

### Change Email Recipient

Edit in `app.py`:
```python
NOTIFICATION_EMAIL = "your_email@example.com"
```

### Modify Active Formula

Current formula: `active = 1 if quantity > 3 else 0`

To change threshold, edit in the `process_stock_report` function.

## Support

For issues or questions:
- Check the logs in the Streamlit interface
- Verify file format matches requirements
- Ensure template file is available

## Template File

The app requires the template file:
`/mnt/user-data/uploads/Laila_Mart_is6o.csv`

Make sure this file is available before running the app.

## Version

Version: 1.0.0
Last Updated: February 2026
