import ftplib
import os

FTP_HOST = "panel.freehosting.com"
FTP_USER = "healthyc"
FTP_PASS = "5xll096QjQ"
LOCAL_DIR = r"e:\ClearClaim\website"

def force_deploy():
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd("/domains/healthyclaim.com/public_html")
        print("Connected and in correct directory.")
        
        # Try to delete existing files to force overwrite
        for file in ["index.html", "style.css"]:
            try:
                ftp.delete(file)
                print(f"Deleted old {file}")
            except Exception as e:
                pass
                
        # Upload index.html and style.css
        for file in ["index.html", "style.css"]:
            local_path = os.path.join(LOCAL_DIR, file)
            print(f"Uploading {file} from {local_path} (Size: {os.path.getsize(local_path)} bytes)")
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {file}", f)
                print(f"Uploaded {file}")
                
        # List to verify
        print("\nVerifying contents:")
        ftp.retrlines('LIST')
        
        ftp.quit()
    except Exception as e:
        print(f"Deployment failed: {e}")

if __name__ == "__main__":
    force_deploy()
