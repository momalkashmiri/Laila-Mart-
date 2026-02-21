"""
Laila Mart Stock Report Processor
Converts daily stock reports to standardized format and uploads to SFTP server.
"""

import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Laila Mart Stock Processor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Main header always looks good ── */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%);
        padding: 2rem; border-radius: 12px; text-align: center;
        color: white !important; margin-bottom: 2rem;
    }
    .main-header h1, .main-header p { color: white !important; }

    /* ── Metric cards — light & dark aware ── */
    .metric-card {
        border-radius: 10px; padding: 1.2rem;
        border-left: 4px solid #2d6a9f;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        text-align: center;
        background: var(--background-color, white);
    }
    .metric-value { font-size: 2rem; font-weight: bold; }
    .metric-label { font-size: 0.85rem; margin-top: 0.3rem; opacity: 0.75; }

    /* ── Success box ── */
    .success-box {
        border: 2px solid #22c55e;
        border-radius: 10px; padding: 1.5rem; margin: 1rem 0;
        background: rgba(34, 197, 94, 0.1);
    }
    .success-box h3 { color: #22c55e !important; }

    /* ── Error box ── */
    .error-box {
        border: 2px solid #ef4444;
        border-radius: 10px; padding: 1.5rem; margin: 1rem 0;
        background: rgba(239, 68, 68, 0.1);
    }
    .error-box h3 { color: #ef4444 !important; }

    /* ── Info box ── */
    .info-box {
        border: 2px solid #3b82f6;
        border-radius: 10px; padding: 1.5rem; margin: 1rem 0;
        background: rgba(59, 130, 246, 0.1);
    }
    .info-box strong { color: #3b82f6 !important; }
    .info-box code {
        background: rgba(59,130,246,0.15);
        padding: 2px 6px; border-radius: 4px;
        font-size: 0.85rem;
    }

    /* ── Footer ── */
    footer { text-align: center; padding: 2rem; font-size: 0.8rem; opacity: 0.6; }
    footer a { color: #3b82f6; }

    /* ── Dark mode metric value colors ── */
    @media (prefers-color-scheme: dark) {
        .metric-card { background: rgba(255,255,255,0.05); }
    }
</style>
""", unsafe_allow_html=True)

# ── Template paths (cloud + local) ────────────────────────────────────────────
TEMPLATE_PATHS = [
    "Laila_Mart_is6o.csv",
    "/mount/src/laila-mart-stock-processor/Laila_Mart_is6o.csv",
    os.path.join(os.path.dirname(__file__), "Laila_Mart_is6o.csv"),
]

OUTPUT_FILENAME = "Laila_Mart_is6o.csv"


# ── Auth helpers ──────────────────────────────────────────────────────────────
def get_credentials():
    try:
        return (
            st.secrets["auth"]["admin_user"],
            st.secrets["auth"]["admin_password"],
        )
    except Exception:
        return "admin", "Naqeeb12345@"


def check_login(username: str, password: str) -> bool:
    valid_user, valid_pass = get_credentials()
    return username == valid_user and password == valid_pass


# ── Template loader ───────────────────────────────────────────────────────────
@st.cache_data
def load_template() -> pd.DataFrame | None:
    for path in TEMPLATE_PATHS:
        if os.path.exists(path):
            df = pd.read_csv(path)
            df["barcode"] = pd.to_numeric(df["barcode"], errors="coerce")
            df = df.dropna(subset=["barcode"])
            df["barcode"] = df["barcode"].astype("int64")
            return df
    return None


# ── File reader ───────────────────────────────────────────────────────────────
def read_stock_report(uploaded_file) -> pd.DataFrame:
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    elif name.endswith(".xls"):
        df = pd.read_excel(uploaded_file, engine="xlrd")
    else:
        raise ValueError(f"Unsupported file type: {uploaded_file.name}")
    return df


# ── Processing logic ──────────────────────────────────────────────────────────
def process_stock_report(stock_df: pd.DataFrame, template_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    # Normalise column names
    stock_df.columns = stock_df.columns.str.strip()

    required = {"Barcode", "Sale Price", "Stock"}
    missing = required - set(stock_df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    # Normalise barcodes in stock report
    stock_df["Barcode"] = pd.to_numeric(stock_df["Barcode"], errors="coerce")
    stock_valid = stock_df.dropna(subset=["Barcode"]).copy()
    stock_valid["Barcode"] = stock_valid["Barcode"].astype("int64")

    # Merge template with stock report (left join → keep all template barcodes)
    merged = template_df[["barcode"]].copy()
    stock_lookup = stock_valid[["Barcode", "Sale Price", "Stock"]].copy()
    stock_lookup.columns = ["barcode", "price", "quantity"]
    stock_lookup["barcode"] = stock_lookup["barcode"].astype("int64")

    result = merged.merge(stock_lookup, on="barcode", how="left")

    # Fill unmatched rows with template values (use dict for safe alignment)
    template_price = template_df.set_index("barcode")["price"]
    template_qty = template_df.set_index("barcode")["quantity"]
    result["price"] = result.apply(
        lambda row: row["price"] if pd.notna(row["price"]) else template_price.get(row["barcode"], 0),
        axis=1,
    )
    result["quantity"] = result.apply(
        lambda row: row["quantity"] if pd.notna(row["quantity"]) else template_qty.get(row["barcode"], 0),
        axis=1,
    )

    # Active formula: IF(quantity > 3, 1, 0)
    result["active"] = (result["quantity"] > 3).astype(int)

    # Final column order
    result = result[["barcode", "price", "active", "quantity"]]

    matched = int(result["barcode"].isin(stock_valid["Barcode"]).sum())
    stats = {
        "total": len(result),
        "matched": matched,
        "unmatched": len(result) - matched,
        "active": int((result["active"] == 1).sum()),
        "inactive": int((result["active"] == 0).sum()),
    }
    return result, stats


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    df = df.copy()
    # Force barcode as plain integer string — prevents scientific notation
    df["barcode"] = df["barcode"].astype("int64").apply(lambda x: str(x))
    df["quantity"] = df["quantity"].apply(lambda x: int(float(x))).astype(str)
    buf = io.StringIO()
    df.to_csv(buf, index=False, quoting=0)
    # Remove any quotes around barcodes
    result = buf.getvalue()
    return result.encode("utf-8")

# ── Email notification ────────────────────────────────────────────────────────
def send_email_notification(stats: dict, source_filename: str, remote_path: str, ts: str, success: bool, error_msg: str = ""):
    try:
        cfg = st.secrets.get("email", {})
        sender = cfg.get("sender_email", "")
        app_password = cfg.get("sender_app_password", "")
        recipients = [r.strip() for r in cfg.get("notification_emails", "").split(",") if r.strip()]

        if not sender or not app_password or not recipients:
            return False, "Email credentials not configured"

        subject = f"✅ Laila Mart Upload SUCCESS - {ts}" if success else f"❌ Laila Mart Upload FAILED - {ts}"

        if success:
            body = f"""
<html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<div style="background: #1e3a5f; padding: 20px; border-radius: 8px 8px 0 0;">
  <h2 style="color: white; margin: 0;">✅ Stock Report Uploaded Successfully</h2>
</div>
<div style="background: #f8fafc; padding: 20px; border: 1px solid #e2e8f0; border-radius: 0 0 8px 8px;">
  <table style="width: 100%; border-collapse: collapse;">
    <tr><td style="padding: 8px; color: #64748b;">📄 Source File</td><td style="padding: 8px; font-weight: bold;">{source_filename}</td></tr>
    <tr style="background:#fff;"><td style="padding: 8px; color: #64748b;">📦 Total Items</td><td style="padding: 8px; font-weight: bold;">{stats["total"]:,}</td></tr>
    <tr><td style="padding: 8px; color: #64748b;">🟢 Active Items</td><td style="padding: 8px; font-weight: bold; color: #16a34a;">{stats["active"]:,}</td></tr>
    <tr style="background:#fff;"><td style="padding: 8px; color: #64748b;">🔴 Inactive Items</td><td style="padding: 8px; font-weight: bold; color: #dc2626;">{stats["inactive"]:,}</td></tr>
    <tr><td style="padding: 8px; color: #64748b;">🕐 Upload Time</td><td style="padding: 8px; font-weight: bold;">{ts}</td></tr>
    <tr style="background:#fff;"><td style="padding: 8px; color: #64748b;">📂 Server Path</td><td style="padding: 8px; font-size: 12px;">{remote_path}</td></tr>
  </table>
  <p style="color: #64748b; font-size: 12px; margin-top: 20px;">This is an automated notification from Laila Mart Stock Processor.</p>
</div>
</body></html>
"""
        else:
            body = f"""
<html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
<div style="background: #dc2626; padding: 20px; border-radius: 8px 8px 0 0;">
  <h2 style="color: white; margin: 0;">❌ Stock Report Upload FAILED</h2>
</div>
<div style="background: #fef2f2; padding: 20px; border: 1px solid #fecaca; border-radius: 0 0 8px 8px;">
  <p><strong>File:</strong> {source_filename}</p>
  <p><strong>Time:</strong> {ts}</p>
  <p><strong>Error:</strong> {error_msg}</p>
  <p style="color: #64748b; font-size: 12px;">Please check your SFTP credentials and try again.</p>
</div>
</body></html>
"""

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.sendmail(sender, recipients, msg.as_string())

        return True, f"Email sent to {', '.join(recipients)}"
    except Exception as e:
        return False, f"Email failed: {e}"




# ── Login page ────────────────────────────────────────────────────────────────
def render_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class='main-header'>
            <h1>📊 Laila Mart</h1>
            <p>Stock Report Processor</p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🔐 Login")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")


# ── Main app ──────────────────────────────────────────────────────────────────
def render_app():
    # Header
    st.markdown(f"""
    <div class='main-header'>
        <h1>📊 Laila Mart Stock Report Processor</h1>
        <p>Convert · Validate · Upload</p>
    </div>
    """, unsafe_allow_html=True)

    # Top bar
    col_title, col_logout = st.columns([8, 1])
    with col_logout:
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Load template
    template_df = load_template()
    if template_df is None:
        st.error("❌ Template file (Laila_Mart_is6o.csv) not found. Please ensure it is in the app directory.")
        return

    # ── Instructions ──────────────────────────────────────────────────────────
    with st.expander("📋 Instructions", expanded=False):
        st.markdown("""
        **How to use this tool:**
        1. Upload your daily stock report (`.xls`, `.xlsx`, or `.csv`)
        2. The file must contain columns: **Barcode**, **Sale Price**, **Stock**
        3. Click **Process Stock Report**
        4. Review the summary metrics and data preview
        5. **Download** the converted file or **Upload to Server** directly
        
        **Processing rules:**
        - All template barcodes are preserved in the output
        - `Sale Price` → `price`, `Stock` → `quantity`
        - `active` = 1 if quantity > 3, else 0
        - Barcodes are stored as numbers
        """)

    st.divider()

    # ── File Upload ───────────────────────────────────────────────────────────
    st.subheader("📁 Upload Stock Report")
    uploaded_file = st.file_uploader(
        "Drag and drop or browse",
        type=["xls", "xlsx", "csv"],
        help="Supported formats: .xls, .xlsx, .csv",
    )

    if uploaded_file:
        st.info(f"📄 File loaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

        if st.button("⚙️ Process Stock Report", type="primary", use_container_width=True):
            with st.spinner("Processing..."):
                try:
                    stock_df = read_stock_report(uploaded_file)
                    result_df, stats = process_stock_report(stock_df, template_df)
                    csv_bytes = df_to_csv_bytes(result_df)

                    st.session_state.result_df = result_df
                    st.session_state.csv_bytes = csv_bytes
                    st.session_state.stats = stats
                    st.session_state.source_filename = uploaded_file.name
                    st.session_state.processed = True
                    st.success("✅ Processing complete!")
                except Exception as e:
                    st.error(f"❌ Processing failed: {e}")
                    st.session_state.processed = False

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.get("processed"):
        result_df = st.session_state.result_df
        stats = st.session_state.stats
        csv_bytes = st.session_state.csv_bytes
        source_filename = st.session_state.source_filename

        st.divider()
        st.subheader("📊 Processing Summary")

        c1, c2, c3, c4 = st.columns(4)
        metrics = [
            (c1, "📦 Total Items", stats["total"], "#1e3a5f"),
            (c2, "✅ Matched", stats["matched"], "#16a34a"),
            (c3, "🟢 Active", stats["active"], "#2563eb"),
            (c4, "🔴 Inactive", stats["inactive"], "#dc2626"),
        ]
        for col, label, value, color in metrics:
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value' style='color:{color}'>{value:,}</div>
                    <div class='metric-label'>{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # Preview
        st.subheader("👁️ Data Preview (first 20 rows)")
        st.dataframe(result_df.head(20), use_container_width=True, hide_index=True)

        st.divider()

        # Upload destination info
        try:
            remote_path = st.secrets["ftp"]["remote_path"]
            host = st.secrets["ftp"]["host"]
        except Exception:
            remote_path = "/vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/catalog"
            host = "vendor-automation-sftp-live-ap.prod.aws.qcommerce.live"

        st.markdown(f"""
        <div class='info-box'>
            <strong>📤 Upload Destination</strong><br>
            🌐 Server: <code>{host}</code><br>
            📂 Path: <code>{remote_path}/{OUTPUT_FILENAME}</code>
        </div>
        """, unsafe_allow_html=True)

        col_dl, col_up = st.columns(2)

        with col_dl:
            st.download_button(
                label="⬇️ Download Converted File",
                data=csv_bytes,
                file_name=OUTPUT_FILENAME,
                mime="text/csv",
                use_container_width=True,
            )

        with col_up:
            if st.button("📤 Upload to Server", type="primary", use_container_width=True):
                with st.spinner("Connecting to SFTP server..."):
                    from sftp_helper import upload_to_sftp
                    try:
                        ftp_cfg = st.secrets.get("ftp", {})
                        success, message, details = upload_to_sftp(
                            file_bytes=csv_bytes,
                            filename=OUTPUT_FILENAME,
                            host=ftp_cfg.get("host", host),
                            port=int(ftp_cfg.get("port", 22)),
                            username=ftp_cfg.get("username", ""),
                            password=ftp_cfg.get("password", ""),
                            remote_path=ftp_cfg.get("remote_path", remote_path),
                        )
                        if success:
                            st.balloons()
                            file_kb = len(csv_bytes) / 1024
                            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            # Send email notification
                            email_ok, email_msg = send_email_notification(
                                stats=stats,
                                source_filename=source_filename,
                                remote_path=details.get("full_path", remote_path),
                                ts=ts,
                                success=True,
                            )
                            if email_ok:
                                st.success(f"📧 Email notification sent!")
                            else:
                                st.warning(f"📧 Email not sent: {email_msg}")

                            st.markdown(f"""
                            <div class='success-box'>
                                <h3>✅ Upload Successful!</h3>
                                <p>{message}</p>
                            </div>
                            """, unsafe_allow_html=True)

                            with st.expander("📋 Upload Details", expanded=True):
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.metric("File Size", f"{file_kb:.1f} KB")
                                    st.metric("Total Items", f"{stats['total']:,}")
                                    st.metric("Active Items", f"{stats['active']:,}")
                                    st.metric("Timestamp", ts)
                                with col_b:
                                    st.metric("Server", details.get("host", host))
                                    st.markdown(f"**Full Path:**\n```\n{details.get('full_path', '')}\n```")
                                    st.markdown(f"**Source File:**\n`{source_filename}`")
                                    st.markdown(f"**FileZilla Verification:**\n```\n{details.get('full_path', '')}\n```")

                            # Upload history
                            if "upload_history" not in st.session_state:
                                st.session_state.upload_history = []
                            st.session_state.upload_history.insert(0, {
                                "Time": ts,
                                "Source File": source_filename,
                                "Items": stats["total"],
                                "Active": stats["active"],
                                "Size (KB)": f"{file_kb:.1f}",
                                "Status": "✅ Success",
                            })
                            st.session_state.upload_history = st.session_state.upload_history[:10]
                        else:
                            # Send failure email
                            send_email_notification(
                                stats=stats,
                                source_filename=source_filename,
                                remote_path=remote_path,
                                ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                success=False,
                                error_msg=message,
                            )
                            st.markdown(f"""
                            <div class='error-box'>
                                <h3>❌ Upload Failed</h3>
                                <p>{message}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            with st.expander("🔧 Troubleshooting Tips"):
                                st.markdown("""
                                **Common solutions:**
                                - **Directory doesn't exist**: The catalog directory may need to be created manually on the server.
                                - **Permission denied**: Check that your SFTP user has write permissions to the target path.
                                - **Connection timeout**: Verify the server hostname and port (22) are reachable.
                                - **Authentication failed**: Double-check the username and password in Streamlit secrets.
                                - **Check secrets.toml**: Ensure all SFTP credentials are correctly configured.
                                """)
                    except Exception as e:
                        st.error(f"❌ SFTP error: {e}")

    # ── Upload History ────────────────────────────────────────────────────────
    if st.session_state.get("upload_history"):
        st.divider()
        st.subheader("📜 Upload History (this session)")
        history_df = pd.DataFrame(st.session_state.upload_history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)

    # Footer
    st.markdown("""
    <footer>
        Laila Mart Stock Processor · Built with Streamlit · 
        <a href='mailto:lailavegetableoil1@gmail.com'>Support</a>
    </footer>
    """, unsafe_allow_html=True)


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        render_login()
    else:
        render_app()


if __name__ == "__main__":
    main()
