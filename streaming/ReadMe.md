# ReadMe of Twitter Streaming

This Folder is built for the purpose to stream Tweets from Twitter-Api. It gets the newest Tweets from a predefined search_key, which will be running 
until the process is finished manually.

THe data will be collected and saved in the "data" folder. Then the files will be concatenated to one big .csv file. This process will be performed each minute to 
ensure to have the latest tweets. 

Pay attention to the Rate Limits, which is with v.1.1 API of Twitter 15 requests per 15 minutes. You can get further information to the Rate Limits here: https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits 

If enough tweets have been collected then the file gdriveupload can be executed to upload the files to a certain Google Drive folder. This needs to be adapted first with a correct 
folder ID changed to one in your personal GoogleDrive Account. Afterwards you can download id with the pyhton file "load_online.py". Here again the correct folder ID needs to be replaced and full access rights given to users with access to the folder link.

## Procedure for the Usage

1. Type in your preferred search key for Twitter in the "executable.py"
2. Save your Twitter-API Credentials in the same folder of the "executable.py" with following structure:
![image info](./img/creds_yaml_structure.PNG =250x)

3. Save your GoogleDrive API Credentials to the folder "integrate" (not necessary if local storage is preferred):
![image info](./img/json_google_drive.PNG =250x)

4. Run the "executable.py" python script.
5. Collection of Tweets starts.


**Further Links:**
- Get your Twitter-API Keys from here: https://developer.twitter.com/en/portal/dashboard

- Further information to Google Drive API: https://developers.google.com/drive/api/v3/enable-drive-api
