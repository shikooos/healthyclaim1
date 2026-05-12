import ftplib
import os

FTP_HOST = "panel.freehosting.com"
# Try the main DirectAdmin user first
FTP_USER = "healthyc"
FTP_PASS = "5xll096QjQ"

LOCAL_DIR = r"e:\ClearClaim\website"

def upload_dir(ftp, local_path, remote_path):
    print(f"Entering directory: {remote_path}")
    try:
        ftp.mkd(remote_path)
    except ftplib.error_perm:
        pass # Directory might already exist

    ftp.cwd(remote_path)

    for item in os.listdir(local_path):
        if item.startswith('.') or item == 'deploy.py':
            continue
            
        local_item = os.path.join(local_path, item)
        if os.path.isfile(local_item):
            print(f"Uploading file: {item}")
            with open(local_item, "rb") as f:
                ftp.storbinary(f"STOR {item}", f)
        elif os.path.isdir(local_item):
            upload_dir(ftp, local_item, item)
            ftp.cwd("..")

def deploy():
    try:
        print(f"Connecting to FTP: {FTP_HOST} as {FTP_USER}")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("Connected.")
        
        # Navigate to the correct web root
        target_dirs = ["domains/healthyclaim.com/public_html", "/public_html", "/"]
        changed = False
        for td in target_dirs:
            try:
                ftp.cwd(td)
                changed = True
                print(f"Navigated to: {td}")
                break
            except ftplib.error_perm:
                pass
                
        if not changed:
             print("Could not navigate to public_html. Uploading to current directory.")
             
        print(f"Current remote directory: {ftp.pwd()}")
        
        # Upload all files
        for item in os.listdir(LOCAL_DIR):
            if item.startswith('.') or item == 'deploy.py':
                continue
                
            local_item = os.path.join(LOCAL_DIR, item)
            if os.path.isfile(local_item):
                print(f"Uploading file: {item}")
                with open(local_item, "rb") as f:
                    ftp.storbinary(f"STOR {item}", f)
            elif os.path.isdir(local_item):
                upload_dir(ftp, local_item, item)
                
        ftp.quit()
        print("Deployment successful.")
    except Exception as e:
        print(f"Deployment failed: {e}")

if __name__ == "__main__":
    deploy()
