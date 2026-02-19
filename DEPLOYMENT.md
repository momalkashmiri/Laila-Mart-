# Deployment Guide - Laila Mart Stock Converter

## 🚀 Quick Deploy to Streamlit Cloud (Recommended - FREE)

### Step 1: Prepare GitHub Repository

1. Create a new repository on GitHub
2. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `sftp_helper.py`
   - `README.md`
   - `Laila_Mart_is6o.csv` (your template file)

### Step 2: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `app.py`
6. Click "Deploy"
7. Wait 2-3 minutes for deployment

### Step 3: Configure Secrets (Important!)

In Streamlit Cloud:
1. Go to App Settings → Secrets
2. Add this configuration:

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
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "your_email@gmail.com"
smtp_password = "your_app_password"
```

### Step 4: Get Your App URL

After deployment, you'll get a URL like:
`https://your-app-name.streamlit.app`

Share this URL with your team!

---

## 💻 Local Development

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## 🐳 Docker Deployment (Advanced)

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build
docker build -t laila-mart-converter .

# Run
docker run -p 8501:8501 laila-mart-converter
```

---

## 🌐 Deploy to Your Own Server

### Ubuntu/Linux Server

```bash
# 1. Install Python and pip
sudo apt update
sudo apt install python3 python3-pip

# 2. Upload your files
scp -r /path/to/app/* user@your-server:/home/user/laila-mart-app/

# 3. SSH into server
ssh user@your-server

# 4. Install dependencies
cd /home/user/laila-mart-app
pip3 install -r requirements.txt

# 5. Run with nohup (keeps running after logout)
nohup streamlit run app.py --server.port=8080 &

# 6. Access via
# http://your-server-ip:8080
```

### Using systemd (Auto-restart on server reboot)

Create `/etc/systemd/system/laila-mart.service`:

```ini
[Unit]
Description=Laila Mart Stock Converter
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/home/user/laila-mart-app
ExecStart=/usr/local/bin/streamlit run app.py --server.port=8080
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable laila-mart
sudo systemctl start laila-mart
```

---

## 🔧 Configuration Tips

### 1. Update Template File Path

If deploying to cloud, update in `app.py`:

```python
# Instead of local path
template_path = "/mnt/user-data/uploads/Laila_Mart_is6o.csv"

# Use relative path
template_path = "Laila_Mart_is6o.csv"
```

### 2. Enable HTTPS

For Streamlit Cloud, HTTPS is automatic.

For your own server:
- Use Nginx reverse proxy with Let's Encrypt SSL
- Or use Cloudflare

### 3. Custom Domain

**Streamlit Cloud:**
1. Go to App Settings
2. Add custom domain (requires DNS configuration)

**Own Server:**
1. Point domain A record to server IP
2. Configure Nginx reverse proxy

---

## 📧 Email Configuration (Gmail)

### Enable App Password

1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Generate App Password
4. Use this password in secrets configuration

### Update app.py

Add email sending function using your SMTP credentials.

---

## 🔐 Security Best Practices

1. **Never commit secrets to GitHub**
   - Use `.gitignore` to exclude sensitive files
   - Use environment variables or Streamlit secrets

2. **Change default passwords**
   - Update admin password immediately
   - Use strong passwords

3. **Enable HTTPS**
   - Always use HTTPS in production
   - Streamlit Cloud provides this automatically

4. **Limit access**
   - Use authentication (already implemented)
   - Consider IP whitelisting for extra security

---

## 📊 Monitoring

### Streamlit Cloud

- View logs in Streamlit Cloud dashboard
- Monitor app usage and errors

### Own Server

```bash
# View logs
journalctl -u laila-mart -f

# Check status
systemctl status laila-mart
```

---

## 🆘 Troubleshooting

### App won't start
```bash
# Check Python version (need 3.8+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### SFTP upload fails
- Verify credentials
- Check network connectivity
- Test with `sftp_helper.test_sftp_connection()`

### Template file not found
- Ensure file is in correct location
- Check file permissions
- Update path in code if needed

---

## 📱 Mobile Access

The app is mobile-friendly! Access from any device:
- iPhone/iPad: Use Safari or Chrome
- Android: Use Chrome or Firefox
- Works on tablets too

---

## 🔄 Updates & Maintenance

### Update the app

**Streamlit Cloud:**
- Push changes to GitHub
- App auto-redeploys

**Own Server:**
```bash
cd /home/user/laila-mart-app
git pull
sudo systemctl restart laila-mart
```

---

## 💡 Next Steps

After deployment:

1. ✅ Test with sample stock report
2. ✅ Verify FTP upload works
3. ✅ Test email notifications
4. ✅ Share URL with team
5. ✅ Set up regular backups
6. ✅ Monitor usage and errors

---

**Need help?** Check the logs or contact support.
