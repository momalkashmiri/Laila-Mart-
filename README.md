# 📊 Laila Mart Stock Report Processor

A Streamlit web application that converts daily stock reports into a standardized format and uploads them directly to an SFTP server.

## Features

- 🔐 Secure login (credentials stored in Streamlit secrets)
- 📁 Upload `.xls`, `.xlsx`, or `.csv` stock reports
- ⚙️ Automatic processing: barcode matching, price mapping, active status calculation
- 👁️ Data preview (first 20 rows)
- ⬇️ Download converted file
- 📤 One-click SFTP upload with confirmation
- 🎈 Visual celebration on successful upload
- 📜 Session upload history (last 10 uploads)

## Input File Requirements

Your daily stock report must contain these columns:

| Column | Description |
|--------|-------------|
| `Barcode` | Product barcode (numeric) |
| `Sale Price` | Current selling price |
| `Stock` | Current stock quantity |

## Output File

**Filename:** `Laila_Mart_is6o.csv`

| Column | Description |
|--------|-------------|
| `barcode` | Numeric barcode |
| `price` | Sale price |
| `active` | 1 if quantity > 3, else 0 |
| `quantity` | Stock quantity |

## Processing Logic

1. Load the template (`Laila_Mart_is6o.csv`) — this contains all barcodes
2. Match incoming barcodes from the stock report
3. Copy `Sale Price` → `price` and `Stock` → `quantity`
4. Calculate `active = 1 if quantity > 3 else 0`
5. All template barcodes are kept (unmatched rows retain template values)

## Quick Start (Local)

```bash
git clone <your-repo-url>
cd laila-mart-stock-processor
pip install -r requirements.txt
streamlit run app.py
```

## Secrets Configuration

Create `.streamlit/secrets.toml` (do **not** commit this file):

```toml
[ftp]
host = "vendor-automation-sftp-live-ap.prod.aws.qcommerce.live"
port = 22
username = "YOUR_SFTP_USERNAME"
password = "YOUR_SFTP_PASSWORD"
remote_path = "/vendor-automation-sftp-storage-live-ap-1/home/YOUR_USERNAME/catalog"

[auth]
admin_user = "admin"
admin_password = "YOUR_PASSWORD"

[email]
notification_email = "your@email.com"
```

## File Structure

```
laila-mart-stock-processor/
├── app.py                    # Main Streamlit application
├── sftp_helper.py            # SFTP upload utilities
├── Laila_Mart_is6o.csv       # Barcode template file
├── requirements.txt          # Python dependencies
├── runtime.txt               # Python version
├── .python-version           # Python version (pyenv)
├── .gitignore                # Excludes secrets & temp files
├── README.md                 # This file
├── DEPLOYMENT.md             # Deployment guide
└── TROUBLESHOOTING.md        # Common issues & fixes
```
