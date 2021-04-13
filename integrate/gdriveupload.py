from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
import time

def gdrive_auth():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    return gauth


def gdrive_upload():
    """
    This funtion uploads files to Google Drive folder given by ID.    
    """
    filepath = os.listdir('../data/')
    
    # AUthentication for drive
    gauth = gdrive_auth()
    drive = GoogleDrive(auth=gauth)
    
    # Folder ID for upload
    folder_id = '1V_HFjIvJqTBQ9f_2GwULJ3UnACBME4lk'
    
    # Upload to drive
    f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}]})
    f.SetContentFile(filepath)
    f.Upload()
    
    
if __name__ == '__main__':
    
    gdrive_upload()
    
    print('Files uploaded to GDrive.')
    time.sleep(2)
    
    
    