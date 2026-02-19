"""
SFTP Upload Helper for Laila Mart Stock Converter
"""

import paramiko
import io
from datetime import datetime

def upload_to_sftp(csv_content, filename, host, port, username, password, remote_path="/"):
    """
    Upload CSV file to SFTP server
    
    Args:
        csv_content: String content of the CSV file
        filename: Name of the file to upload
        host: SFTP host (without sftp:// prefix)
        port: SFTP port (usually 22)
        username: SFTP username
        password: SFTP password
        remote_path: Remote directory path
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Clean host (remove sftp:// if present)
        if host.startswith('sftp://'):
            host = host.replace('sftp://', '')
        
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to SFTP server
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=30
        )
        
        # Open SFTP session
        sftp = ssh.open_sftp()
        
        # Convert string content to file-like object
        file_obj = io.BytesIO(csv_content.encode('utf-8'))
        
        # Construct remote file path
        remote_file = f"{remote_path.rstrip('/')}/{filename}"
        
        # Upload file
        sftp.putfo(file_obj, remote_file)
        
        # Close connections
        sftp.close()
        ssh.close()
        
        upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return True, f"File uploaded successfully to {remote_file} at {upload_time}"
        
    except paramiko.AuthenticationException:
        return False, "Authentication failed. Please check username and password."
    except paramiko.SSHException as e:
        return False, f"SSH connection error: {str(e)}"
    except Exception as e:
        return False, f"Upload failed: {str(e)}"

def test_sftp_connection(host, port, username, password):
    """
    Test SFTP connection
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Clean host
        if host.startswith('sftp://'):
            host = host.replace('sftp://', '')
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=10
        )
        
        ssh.close()
        return True, "Connection successful!"
        
    except Exception as e:
        return False, f"Connection failed: {str(e)}"
