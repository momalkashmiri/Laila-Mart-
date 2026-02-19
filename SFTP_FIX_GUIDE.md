# SFTP Upload Fix Guide

## Issue
File is being uploaded to the wrong directory - it's in the home directory instead of the `/catalog` subdirectory.

## Root Cause
The `catalog` directory might not exist, or there might be permission issues.

## Solutions

### Solution 1: Run Debug Script (Recommended First Step)

This will help us understand the exact issue:

```bash
python debug_sftp.py
```

This script will:
- ✅ Test connection
- ✅ Show current directory structure
- ✅ Check if catalog directory exists
- ✅ Try to create catalog directory
- ✅ Test file upload
- ✅ Show exactly where files are going

### Solution 2: Manually Create Catalog Directory

If the debug script shows the catalog directory doesn't exist:

**Option A: Using SFTP Client (FileZilla/WinSCP)**
1. Connect to your SFTP server
2. Navigate to: `/vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/`
3. Create a new folder named `catalog`
4. Set permissions to allow write access

**Option B: Using Command Line**
```bash
sftp FP_PK_aca38750-f6ba-464a-9316-87415735d1e3@vendor-automation-sftp-live-ap.prod.aws.qcommerce.live
# Enter password: zCGKp?{52IRsya$Wxj|!>U
cd /vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/
mkdir catalog
exit
```

### Solution 3: Verify Correct Path

Double-check the upload path from your screenshot:

**Current (wrong):** 
```
/vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/Laila_Mart_is6o.csv
```

**Should be:**
```
/vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/catalog/Laila_Mart_is6o.csv
```

### Solution 4: Alternative Upload Path

If you cannot create the catalog directory, you can modify the upload path:

**Edit app.py line 24:**

**Current:**
```python
FTP_UPLOAD_DIR = "/vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3/catalog"
```

**Change to (upload to home directory):**
```python
FTP_UPLOAD_DIR = "/vendor-automation-sftp-storage-live-ap-1/home/FP_PK_aca38750-f6ba-464a-9316-87415735d1e3"
```

Or even simpler (use current working directory):
```python
FTP_UPLOAD_DIR = "catalog"
```

### Solution 5: Check Permissions

The issue might be permissions. To check:

1. **Using debug_sftp.py** - It will show directory permissions
2. **Contact your SFTP provider** - Ask them to:
   - Create the `catalog` directory
   - Grant write permissions to your user
   - Verify the correct upload path

## Testing After Fix

After implementing any solution, test with the app:

1. Upload a stock report file
2. Process it
3. Click "Upload to FTP Server"
4. Check the success message - it should show:
   ```
   ✅ File uploaded successfully!
   Path: /vendor-automation-sftp-storage-live-ap-1/home/.../catalog/Laila_Mart_is6o.csv
   ```

## Quick Test Command

Test upload from command line:
```bash
python debug_sftp.py
```

This will show you exactly what's happening and where files are going.

## Common Issues

### Issue 1: "Directory does not exist"
**Fix:** Create the catalog directory manually (Solution 2)

### Issue 2: "Permission denied"
**Fix:** Contact SFTP provider to grant write permissions

### Issue 3: "File uploaded but in wrong location"
**Fix:** Verify the FTP_UPLOAD_DIR path in app.py

### Issue 4: "Cannot create directory"
**Fix:** Use alternative upload path (Solution 4)

## Verification Checklist

After fixing, verify:
- ✅ Catalog directory exists
- ✅ You have write permissions
- ✅ Upload path in app.py is correct
- ✅ File appears in catalog directory after upload
- ✅ File size is correct

## Need Help?

1. **Run debug_sftp.py** - This will give detailed information
2. **Share the debug output** - It will help identify the exact issue
3. **Check SFTP provider documentation** - They might have specific path requirements

## Contact SFTP Provider

If issues persist, ask your SFTP provider:

1. "What is the correct upload path for catalog files?"
2. "Can you create a 'catalog' directory in my home folder?"
3. "Do I have write permissions in the catalog directory?"
4. "What is my default working directory upon login?"

The provider can quickly resolve permission and path issues.
