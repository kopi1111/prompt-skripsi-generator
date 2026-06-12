
# export_handler.py
import os, csv, zipfile
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)

def save_csv(df, base_filename='export'):
    # df is a pandas DataFrame or similar with to_csv method-friendly behavior
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{base_filename}_{timestamp}.csv"
    path = os.path.join('/mnt/data', filename)
    # if df has to_csv (pandas), handle; else assume list of dicts
    try:
        df.to_csv(path, index=False)
    except Exception:
        # fallback: assume iterable of dicts
        with open(path, 'w', newline='', encoding='utf-8') as f:
            if len(df) > 0:
                writer = csv.DictWriter(f, fieldnames=list(df[0].keys()))
                writer.writeheader()
                writer.writerows(df)
    return path

def create_zip_download_link(folder_path, zip_name='export.zip'):
    # Create a zip of the folder and return path
    zip_path = os.path.join('/mnt/data', zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # store relative path in zip
                rel_path = os.path.relpath(file_path, folder_path)
                zf.write(file_path, arcname=rel_path)
    return zip_path
