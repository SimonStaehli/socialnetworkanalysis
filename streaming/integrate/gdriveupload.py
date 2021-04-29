from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
import time
import datetime as dt

def gdrive_auth():
    gauth = GoogleAuth()

    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")

    if gauth.credentials is None:
        # Authenticate if they're not there

        # This is what solved the issues:
        gauth.GetFlow()
        gauth.flow.params.update({'access_type': 'offline'})
        gauth.flow.params.update({'approval_prompt': 'force'})

        gauth.LocalWebserverAuth()

    elif gauth.access_token_expired:

        # Refresh them if expired

        gauth.Refresh()
    else:

        # Initialize the saved creds

        gauth.Authorize()

    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    gauth.LocalWebserverAuth()

    return gauth


def gdrive_upload():
    """
    This funtion uploads files to Google Drive folder given by ID.    
    """
    path_2_dir = '../data/'
    filepath = os.listdir(path_2_dir)
    print(filepath)
    
    # AUthentication for drive
    gauth = gdrive_auth()
    drive = GoogleDrive(auth=gauth)
    
    # Folder ID for upload
    folder_id = '1V_HFjIvJqTBQ9f_2GwULJ3UnACBME4lk'
    
    # Upload to drive
    for file in filepath:
        f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}]})
        f.SetContentFile(path_2_dir + file)
        f['title'] = dt.datetime.now().strftime(format="%y-%m-%d") + '_tweets.csv'
        f.Upload()
    
    
if __name__ == '__main__':
    
    gdrive_upload()
    
    print('Files uploaded to GDrive.')
    time.sleep(2)
    
    
    