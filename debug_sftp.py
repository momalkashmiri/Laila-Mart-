"""
SFTP Upload Debug Script
Use this to test where files are being uploaded and verify paths
"""

import paramiko
import io
from datetime import datetime

# SFTP Configuration
FTP_HOST = "vendor-automation-sftp-live-ap.prod.aws.qcommerce.live"
FTP_PORT = 22
FTP_USER = "FP_PK_aca38750-f6ba-464a-9316-87415735d1e3"
FTP_PASS = "zCGKp?{52IRsya$Wxj|!>U"
FTP_UPLOAD_DIR = "/vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/catalog"

def debug_sftp_upload():
    """
    Debug SFTP upload with detailed information
    """
    print("=" * 70)
    print("SFTP UPLOAD DEBUG SCRIPT")
    print("=" * 70)
    print()
    
    print(f"Host: {FTP_HOST}")
    print(f"Port: {FTP_PORT}")
    print(f"User: {FTP_USER}")
    print(f"Target Directory: {FTP_UPLOAD_DIR}")
    print()
    
    try:
        # Connect to SFTP
        print("Step 1: Connecting to SFTP server...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(
            hostname=FTP_HOST,
            port=FTP_PORT,
            username=FTP_USER,
            password=FTP_PASS,
            timeout=30
        )
        print("✅ Connected successfully!")
        print()
        
        # Open SFTP session
        print("Step 2: Opening SFTP session...")
        sftp = ssh.open_sftp()
        print("✅ SFTP session opened!")
        print()
        
        # List home directory
        print("Step 3: Listing home directory...")
        home_dir = sftp.getcwd() or "/"
        print(f"Current directory: {home_dir}")
        
        try:
            print("\nListing root contents:")
            root_files = sftp.listdir("/")
            for item in root_files[:10]:  # Show first 10 items
                print(f"  - {item}")
        except Exception as e:
            print(f"  Cannot list root: {e}")
        print()
        
        # Check if target directory exists
        print(f"Step 4: Checking if target directory exists...")
        print(f"Target: {FTP_UPLOAD_DIR}")
        
        try:
            stat = sftp.stat(FTP_UPLOAD_DIR)
            print(f"✅ Directory exists!")
            print(f"   Permissions: {oct(stat.st_mode)}")
            print()
            
            # List contents of catalog directory
            print("Contents of catalog directory:")
            try:
                catalog_files = sftp.listdir(FTP_UPLOAD_DIR)
                if catalog_files:
                    for item in catalog_files:
                        print(f"  - {item}")
                else:
                    print("  (empty)")
            except Exception as e:
                print(f"  Cannot list: {e}")
                
        except FileNotFoundError:
            print(f"❌ Directory does not exist!")
            print()
            
            # Try to list parent directory
            parent_dir = "/".join(FTP_UPLOAD_DIR.split("/")[:-1])
            print(f"Checking parent directory: {parent_dir}")
            try:
                parent_files = sftp.listdir(parent_dir)
                print(f"Contents of parent directory:")
                for item in parent_files:
                    print(f"  - {item}")
            except Exception as e:
                print(f"  Cannot list parent: {e}")
                
        except Exception as e:
            print(f"❌ Error checking directory: {e}")
        print()
        
        # Try to create catalog directory if needed
        print("Step 5: Attempting to create catalog directory...")
        try:
            sftp.mkdir(FTP_UPLOAD_DIR)
            print(f"✅ Created directory: {FTP_UPLOAD_DIR}")
        except FileExistsError:
            print(f"✅ Directory already exists")
        except Exception as e:
            print(f"⚠️  Cannot create directory: {e}")
            print("   (This might be okay if you don't have mkdir permissions)")
        print()
        
        # Test upload
        print("Step 6: Testing file upload...")
        test_filename = "test_upload.csv"
        test_content = "barcode,price,active,quantity\n123456,100,1,5\n"
        
        file_obj = io.BytesIO(test_content.encode('utf-8'))
        remote_file = f"{FTP_UPLOAD_DIR}/{test_filename}"
        
        print(f"Uploading to: {remote_file}")
        
        try:
            sftp.putfo(file_obj, remote_file)
            
            # Verify upload
            stat = sftp.stat(remote_file)
            print(f"✅ Upload successful!")
            print(f"   File path: {remote_file}")
            print(f"   File size: {stat.st_size} bytes")
            print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            
            # List directory again to confirm
            print("Verifying - Current catalog contents:")
            catalog_files = sftp.listdir(FTP_UPLOAD_DIR)
            for item in catalog_files:
                file_stat = sftp.stat(f"{FTP_UPLOAD_DIR}/{item}")
                print(f"  - {item} ({file_stat.st_size} bytes)")
                
        except Exception as upload_error:
            print(f"❌ Upload failed: {upload_error}")
        
        # Close connections
        sftp.close()
        ssh.close()
        
        print()
        print("=" * 70)
        print("DEBUG COMPLETE")
        print("=" * 70)
        
    except paramiko.AuthenticationException:
        print("❌ Authentication failed!")
        print("   Check username and password")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_sftp_upload()
