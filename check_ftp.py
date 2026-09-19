import ftplib
import os

FTP_HOST = os.getenv("FTP_HOST", "panel.freehosting.com")
FTP_USER = os.getenv("FTP_USER", "")
FTP_PASS = os.getenv("FTP_PASS", "")

def check_ftp():
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("Connected.")
        
        paths_to_check = [
            "/",
            "/public_html",
            "/domains",
            "/domains/healthyclaim.com",
            "/domains/healthyclaim.com/public_html"
        ]
        
        for path in paths_to_check:
            try:
                ftp.cwd(path)
                print(f"\nContents of {path}:")
                ftp.retrlines('LIST')
            except Exception as e:
                print(f"Error accessing {path}: {e}")
                
        ftp.quit()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check_ftp()
