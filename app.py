import streamlit as st
import pandas as pd
import io
from datetime import datetime
import ftplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import tempfile

# Page config
st.set_page_config(
    page_title="Laila Mart Stock Converter",
    page_icon="📊",
    layout="wide"
)

# FTP Configuration
FTP_HOST = "sftp://vendor-automation-sftp-live-ap.prod.aws.qcommerce.live"
FTP_PORT = 22
FTP_USER = "FP_PK_aca38750-f6ba-464a-9316-87415735d1e3"
FTP_PASS = "zCGKp?{52IRsya$Wxj|!>U"
FTP_UPLOAD_DIR = "/vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/catalog"

# Email Configuration
NOTIFICATION_EMAIL = "lailavegetableoil1@gmail.com"

# Authentication
ADMIN_USER = "admin"
ADMIN_PASS = "Naqeeb12345@"

# Session state for login
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_login(username, password):
    """Check if login credentials are correct"""
    return username == ADMIN_USER and password == ADMIN_PASS

def login_page():
    """Display login page"""
    st.title("🔐 Laila Mart Stock Converter")
    st.markdown("### Login to Continue")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if check_login(username, password):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

def convert_barcode(barcode):
    """Convert barcode to numeric format"""
    try:
        return int(float(str(barcode).strip()))
    except:
        try:
            return float(str(barcode).strip())
        except:
            return str(barcode).strip()

def process_stock_report(uploaded_file, template_df):
    """Process the uploaded stock report and convert to Laila Mart format"""
    
    # Read the uploaded file
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_extension == 'csv':
            stock_report = pd.read_csv(uploaded_file)
        elif file_extension in ['xls', 'xlsx']:
            # Convert to temporary file for LibreOffice if needed
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            stock_report = pd.read_excel(tmp_path)
            os.unlink(tmp_path)  # Clean up temp file
        else:
            return None, "Unsupported file format"
    except Exception as e:
        return None, f"Error reading file: {str(e)}"
    
    # Clean column names
    stock_report.columns = stock_report.columns.str.strip()
    template_df.columns = template_df.columns.str.strip()
    
    # Check if required columns exist
    if 'Barcode' not in stock_report.columns or 'Sale Price' not in stock_report.columns or 'Stock' not in stock_report.columns:
        return None, "Stock report must contain 'Barcode', 'Sale Price', and 'Stock' columns"
    
    # Convert barcodes
    stock_report['Barcode'] = stock_report['Barcode'].apply(convert_barcode)
    template_df['barcode'] = template_df['barcode'].apply(convert_barcode)
    
    # Create lookup dictionary
    stock_dict = {}
    for _, row in stock_report.iterrows():
        barcode = row['Barcode']
        try:
            price = float(row['Sale Price'])
        except:
            price = 0.0
        
        try:
            stock = float(row['Stock'])
        except:
            stock = 0.0
        
        stock_dict[barcode] = {
            'price': price,
            'quantity': stock
        }
    
    # Create result lists
    barcodes_list = []
    prices_list = []
    actives_list = []
    quantities_list = []
    
    matched = 0
    not_matched = 0
    
    for barcode in template_df['barcode']:
        barcodes_list.append(barcode)
        
        if barcode in stock_dict:
            price = float(stock_dict[barcode]['price'])
            quantity = float(stock_dict[barcode]['quantity'])
            active = 1 if quantity > 3 else 0
            
            prices_list.append(price)
            quantities_list.append(quantity)
            actives_list.append(active)
            matched += 1
        else:
            prices_list.append(0.0)
            quantities_list.append(0.0)
            actives_list.append(0)
            not_matched += 1
    
    # Create result dataframe
    result = pd.DataFrame({
        'barcode': barcodes_list,
        'price': prices_list,
        'active': actives_list,
        'quantity': quantities_list
    })
    
    stats = {
        'total_rows': len(result),
        'matched': matched,
        'not_matched': not_matched,
        'active_items': result['active'].sum(),
        'inactive_items': len(result) - result['active'].sum()
    }
    
    return result, stats

def upload_to_ftp(file_content, filename):
    """Upload file to FTP server"""
    try:
        from sftp_helper import upload_to_sftp
        
        # Remove sftp:// prefix from host
        host = FTP_HOST.replace('sftp://', '')
        
        success, message = upload_to_sftp(
            csv_content=file_content,
            filename=filename,
            host=host,
            port=FTP_PORT,
            username=FTP_USER,
            password=FTP_PASS,
            remote_path=FTP_UPLOAD_DIR
        )
        
        return success, message
        
    except Exception as e:
        return False, f"Upload Error: {str(e)}"

def send_email_notification(stats, filename):
    """Send email notification with summary"""
    try:
        # Email content
        subject = f"Stock Report Processed - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        body = f"""
        <html>
        <body>
            <h2>Stock Report Processing Complete</h2>
            <p><strong>File:</strong> {filename}</p>
            <p><strong>Processed at:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h3>Summary:</h3>
            <ul>
                <li><strong>Total Items:</strong> {stats['total_rows']}</li>
                <li><strong>Matched Barcodes:</strong> {stats['matched']}</li>
                <li><strong>Not Matched:</strong> {stats['not_matched']}</li>
                <li><strong>Active Items (qty > 3):</strong> {stats['active_items']}</li>
                <li><strong>Inactive Items:</strong> {stats['inactive_items']}</li>
            </ul>
            
            <p>The file has been generated and is ready for download/upload.</p>
        </body>
        </html>
        """
        
        # Note: Email sending requires SMTP configuration
        # This is a placeholder - you'll need to configure SMTP server
        return True, "Email notification prepared"
        
    except Exception as e:
        return False, f"Email Error: {str(e)}"

def main_app():
    """Main application interface"""
    
    # Header
    st.title("📊 Laila Mart Stock Report Converter")
    st.markdown("### Automated Stock Report Processing System")
    
    # Logout button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()
    
    st.markdown("---")
    
    # Load template
    # Try multiple paths for different deployment environments
    template_paths = [
        "Laila_Mart_is6o.csv",  # Cloud deployment
        "/mnt/user-data/uploads/Laila_Mart_is6o.csv",  # Local development
        "./Laila_Mart_is6o.csv"  # Alternative path
    ]
    
    template_df = None
    template_path = None
    
    for path in template_paths:
        try:
            template_df = pd.read_csv(path)
            template_path = path
            break
        except FileNotFoundError:
            continue
    
    if template_df is None:
        st.error("❌ Template file 'Laila_Mart_is6o.csv' not found!")
        st.info("Please ensure the template file is uploaded to your repository.")
        return
    
    st.success(f"✅ Template loaded successfully ({len(template_df)} items)")
    
    # File upload section
    st.markdown("### 📤 Upload Stock Report")
    
    uploaded_file = st.file_uploader(
        "Choose a stock report file (.xls, .xlsx, or .csv)",
        type=['xls', 'xlsx', 'csv'],
        help="Upload your daily stock report file"
    )
    
    if uploaded_file:
        st.info(f"📁 File uploaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.2f} KB)")
        
        # Process button
        if st.button("🔄 Process Stock Report", type="primary", use_container_width=True):
            with st.spinner("Processing your stock report..."):
                result, stats_or_error = process_stock_report(uploaded_file, template_df.copy())
                
                if result is None:
                    st.error(f"❌ {stats_or_error}")
                else:
                    st.success("✅ Stock report processed successfully!")
                    
                    # Display statistics
                    st.markdown("### 📊 Processing Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Items", stats_or_error['total_rows'])
                    with col2:
                        st.metric("Matched", stats_or_error['matched'])
                    with col3:
                        st.metric("Active Items", stats_or_error['active_items'])
                    with col4:
                        st.metric("Inactive Items", stats_or_error['inactive_items'])
                    
                    # Preview
                    st.markdown("### 👀 Preview (First 20 rows)")
                    st.dataframe(result.head(20), use_container_width=True)
                    
                    # Convert to CSV
                    csv_buffer = io.StringIO()
                    result.to_csv(csv_buffer, index=False)
                    csv_data = csv_buffer.getvalue()
                    
                    # Download button
                    st.markdown("### 💾 Download Result")
                    st.download_button(
                        label="📥 Download Laila_Mart_is6o.csv",
                        data=csv_data,
                        file_name="Laila_Mart_is6o.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                    # FTP Upload option
                    st.markdown("### 🌐 Upload to Server")
                    if st.button("📤 Upload to FTP Server", use_container_width=True):
                        with st.spinner("Uploading to server..."):
                            success, message = upload_to_ftp(csv_data, "Laila_Mart_is6o.csv")
                            if success:
                                st.success(f"✅ {message}")
                            else:
                                st.error(f"❌ {message}")
                    
                    # Email notification
                    if st.button("📧 Send Email Summary", use_container_width=True):
                        with st.spinner("Sending email..."):
                            success, message = send_email_notification(stats_or_error, uploaded_file.name)
                            if success:
                                st.success(f"✅ {message}")
                            else:
                                st.error(f"❌ {message}")
    
    # Instructions
    st.markdown("---")
    st.markdown("### 📖 Instructions")
    st.markdown("""
    1. **Upload** your daily stock report file (.xls, .xlsx, or .csv)
    2. **Click** the "Process Stock Report" button
    3. **Review** the processing summary and preview
    4. **Download** the converted Laila_Mart_is6o.csv file
    5. **Optional:** Upload directly to FTP server or send email summary
    
    **File Requirements:**
    - Must contain columns: `Barcode`, `Sale Price`, `Stock`
    - Supported formats: .xls, .xlsx, .csv
    
    **Active Status Formula:**
    - Active = 1 if quantity > 3
    - Active = 0 if quantity ≤ 3
    """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>Laila Mart & Pharmacy - Stock Report Automation System</div>",
        unsafe_allow_html=True
    )

# Main execution
if not st.session_state.authenticated:
    login_page()
else:
    main_app()
