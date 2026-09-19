import ftplib
import os
import time

FTP_HOST = os.getenv("FTP_HOST", "panel.freehosting.com")
FTP_USER = os.getenv("FTP_USER", "")
FTP_PASS = os.getenv("FTP_PASS", "")
LOCAL_DIR = r"e:\ClearClaim\website"

def connect_ftp():
    print(f"Connecting to FTP: {FTP_HOST} as {FTP_USER}")
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    print("Connected.")
    return ftp

def navigate_to_root(ftp):
    target_dirs = ["domains/healthyclaim.com/public_html", "/public_html", "/"]
    for td in target_dirs:
        try:
            ftp.cwd(td)
            print(f"Navigated to: {td}")
            return td
        except ftplib.error_perm:
            pass
    print("Could not navigate to public_html. Using current directory.")
    return ftp.pwd()

def upload_file_with_retry(ftp_func, local_path, remote_filename, relative_dir_path=""):
    """
    Uploads a file with automatic reconnection and retry logic.
    ftp_func: a callable that returns a fresh or existing active ftp connection
    """
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            ftp = ftp_func()
            
            # Navigate to correct directory
            navigate_to_root(ftp)
            if relative_dir_path:
                for part in relative_dir_path.replace("\\", "/").split("/"):
                    if part:
                        try:
                            ftp.cwd(part)
                        except ftplib.error_perm:
                            ftp.mkd(part)
                            ftp.cwd(part)
            
            local_size = os.path.getsize(local_path)
            
            # Check if remote file exists and has the same size
            try:
                remote_size = ftp.size(remote_filename)
                if remote_size == local_size:
                    print(f"[{remote_filename}] Size matches ({local_size} bytes). Skipping upload.")
                    return True
            except Exception:
                # File might not exist or SIZE command not supported
                pass
            
            print(f"Uploading {remote_filename} (Size: {local_size} bytes)... Attempt {attempt}")
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {remote_filename}", f)
            print(f"Successfully uploaded {remote_filename}")
            return True
            
        except (ftplib.all_errors, ConnectionError, IOError) as e:
            print(f"Error uploading {remote_filename} on attempt {attempt}: {e}")
            if attempt < max_retries:
                print("Waiting 3 seconds before retrying...")
                time.sleep(3)
            else:
                print(f"Failed to upload {remote_filename} after {max_retries} attempts.")
                raise e
    return False

def deploy():
    # We will maintain a single ftp instance ref
    _ftp_instance = None
    
    def get_ftp():
        nonlocal _ftp_instance
        if _ftp_instance is None:
            _ftp_instance = connect_ftp()
        else:
            try:
                _ftp_instance.voidcmd("NOOP")
            except Exception:
                print("FTP connection lost. Reconnecting...")
                try:
                    _ftp_instance.quit()
                except Exception:
                    pass
                _ftp_instance = connect_ftp()
        return _ftp_instance

    try:
        # Collect all files and directories
        all_items = os.listdir(LOCAL_DIR)
        
        # Filter items
        items_to_process = []
        for item in all_items:
            if item.startswith('.') or item in ['deploy.py', 'deploy_logo.py', 'force_deploy.py', 'check_ftp.py']:
                continue
            items_to_process.append(item)
            
        # Group files and directories
        files = []
        dirs = []
        for item in items_to_process:
            full_path = os.path.join(LOCAL_DIR, item)
            if os.path.isfile(full_path):
                files.append(item)
            elif os.path.isdir(full_path):
                dirs.append(item)
                
        # 1. Upload files in the root first (ensures index.html, style.css, etc., go live immediately)
        print("--- Uploading Root Files ---")
        for file in files:
            local_path = os.path.join(LOCAL_DIR, file)
            try:
                upload_file_with_retry(get_ftp, local_path, file)
            except Exception as e:
                print(f"Skipping root file {file} due to failure: {e}")
                
        # 2. Upload directories
        print("\n--- Uploading Directories ---")
        for directory in dirs:
            local_dir_path = os.path.join(LOCAL_DIR, directory)
            # Traverse directory
            for root_path, subdirs, filenames in os.walk(local_dir_path):
                # Calculate relative path from LOCAL_DIR
                rel_path = os.path.relpath(root_path, LOCAL_DIR)
                print(f"Processing directory: {rel_path}")
                
                for filename in filenames:
                    if filename.startswith('.'):
                        continue
                    local_file_path = os.path.join(root_path, filename)
                    try:
                        upload_file_with_retry(get_ftp, local_file_path, filename, rel_path)
                    except Exception as e:
                        print(f"Skipping directory file {rel_path}/{filename} due to failure: {e}")

        # Close final connection
        if _ftp_instance:
            try:
                _ftp_instance.quit()
                print("Disconnected from FTP.")
            except Exception:
                pass
                
        print("\nDeployment process completed.")
    except Exception as e:
        print(f"Deployment process aborted: {e}")

if __name__ == "__main__":
    deploy()
