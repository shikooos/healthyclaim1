import ftplib
import os

FTP_HOST = "panel.freehosting.com"
FTP_USER = "healthyc"
FTP_PASS = "5xll096QjQ"
LOCAL_DIR = r"e:\ClearClaim\website"

def deploy_logo():
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd("/domains/healthyclaim.com/public_html")
        
        file = "healthy-claim-logo.svg"
        local_path = os.path.join(LOCAL_DIR, file)
        
        print(f"Uploading {file} from {local_path} (Size: {os.path.getsize(local_path)} bytes)")
        with open(local_path, "rb") as f:
            ftp.storbinary(f"STOR {file}", f)
            print(f"Uploaded {file} successfully.")
                
        ftp.quit()
    except Exception as e:
        print(f"Deployment failed: {e}")

if __name__ == "__main__":
    deploy_logo()
