"""
sftp_helper.py
SFTP upload utilities for Laila Mart Stock Processor.
"""

import io
import stat
from typing import Tuple


def upload_to_sftp(
    file_bytes: bytes,
    filename: str,
    host: str,
    port: int,
    username: str,
    password: str,
    remote_path: str,
) -> Tuple[bool, str, dict]:
    """
    Upload file_bytes to the SFTP server.

    Returns
    -------
    (success: bool, message: str, details: dict)
    """
    try:
        import paramiko
    except ImportError:
        return False, "paramiko is not installed. Add it to requirements.txt.", {}

    transport = None
    sftp = None

    try:
        # ── Connect ──────────────────────────────────────────────────────────
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # ── Ensure remote directory exists ───────────────────────────────────
        _mkdir_p(sftp, remote_path)

        # ── Upload ───────────────────────────────────────────────────────────
        remote_file = f"{remote_path.rstrip('/')}/{filename}"
        file_obj = io.BytesIO(file_bytes)
        sftp.putfo(file_obj, remote_file)

        # ── Verify size ───────────────────────────────────────────────────────
        remote_stat = sftp.stat(remote_file)
        uploaded_size = remote_stat.st_size

        details = {
            "host": host,
            "full_path": remote_file,
            "remote_size_bytes": uploaded_size,
        }

        return (
            True,
            f"File uploaded successfully to {remote_file} ({uploaded_size / 1024:.1f} KB)",
            details,
        )

    except paramiko.AuthenticationException:
        return False, "Authentication failed. Check your SFTP username and password.", {}
    except paramiko.SSHException as e:
        return False, f"SSH/SFTP connection error: {e}", {}
    except FileNotFoundError as e:
        return False, f"Remote path issue: {e}", {}
    except PermissionError as e:
        return False, f"Permission denied on server: {e}", {}
    except Exception as e:
        return False, f"Upload failed: {type(e).__name__}: {e}", {}
    finally:
        if sftp:
            try:
                sftp.close()
            except Exception:
                pass
        if transport:
            try:
                transport.close()
            except Exception:
                pass


def _mkdir_p(sftp, remote_path: str):
    """Recursively create remote directories (like mkdir -p)."""
    dirs = []
    path = remote_path
    while True:
        try:
            sftp.stat(path)
            break  # exists
        except FileNotFoundError:
            dirs.append(path)
            parent = path.rsplit("/", 1)[0]
            if not parent or parent == path:
                break
            path = parent

    for directory in reversed(dirs):
        try:
            sftp.mkdir(directory)
        except Exception:
            pass  # may already exist due to race condition


def test_sftp_connection(host: str, port: int, username: str, password: str) -> Tuple[bool, str]:
    """Test SFTP connectivity without uploading."""
    try:
        import paramiko
    except ImportError:
        return False, "paramiko not installed"

    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        transport.close()
        return True, f"Connected to {host}:{port} successfully"
    except Exception as e:
        return False, f"Connection test failed: {e}"
