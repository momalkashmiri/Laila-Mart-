"""
Test SFTP Connection Script
Run this to verify your SFTP credentials and connection before deploying
"""

from sftp_helper import test_sftp_connection, upload_to_sftp
import sys

# SFTP Configuration
FTP_HOST = "vendor-automation-sftp-live-ap.prod.aws.qcommerce.live"
FTP_PORT = 22
FTP_USER = "FP_PK_aca38750-f6ba-464a-9316-87415735d1e3"
FTP_PASS = "zCGKp?{52IRsya$Wxj|!>U"
FTP_UPLOAD_DIR = "/vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/catalog"

def main():
    print("=" * 60)
    print("SFTP Connection Test")
    print("=" * 60)
    print()
    
    print(f"Host: {FTP_HOST}")
    print(f"Port: {FTP_PORT}")
    print(f"User: {FTP_USER}")
    print(f"Upload Directory: {FTP_UPLOAD_DIR}")
    print()
    
    print("Testing connection...")
    print("-" * 60)
    
    success, message = test_sftp_connection(
        host=FTP_HOST,
        port=FTP_PORT,
        username=FTP_USER,
        password=FTP_PASS
    )
    
    if success:
        print(f"✅ {message}")
        print()
        
        # Test upload with a sample file
        print("Testing file upload...")
        print("-" * 60)
        
        test_content = "barcode,price,active,quantity\n123456,100,1,5\n"
        
        upload_success, upload_message = upload_to_sftp(
            csv_content=test_content,
            filename="test_upload.csv",
            host=FTP_HOST,
            port=FTP_PORT,
            username=FTP_USER,
            password=FTP_PASS,
            remote_path=FTP_UPLOAD_DIR
        )
        
        if upload_success:
            print(f"✅ {upload_message}")
            print()
            print("🎉 SFTP connection and upload working perfectly!")
            return 0
        else:
            print(f"❌ Upload failed: {upload_message}")
            return 1
    else:
        print(f"❌ Connection failed: {message}")
        print()
        print("Please check:")
        print("  1. Network connectivity")
        print("  2. Credentials are correct")
        print("  3. Server is accessible")
        return 1

if __name__ == "__main__":
    sys.exit(main())
