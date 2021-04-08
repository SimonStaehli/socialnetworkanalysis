import pandas as pd
from read_transform import transform
import requests
from bs4 import BeautifulSoup
import time


def get_drive_content(drive_url):
    """
    Extracts all documents (mainly csv) documents from Google drive with dependent ID for download directly
    from Google Drive. Drive FOlder should be available to anyone.

    @param drive_url: Url to GDrive Folder
    @return: Dictionary with Name of Doc and ID
    """
    response = requests.get(drive_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract doc titles
    parsed_html = soup.find_all('div', attrs={'class': 'Q5txwe'})
    doc_titles = []
    for content in parsed_html:
        doc_titles.append(content.text)

    # Extract Doc-ID's
    parsed_html = soup.find_all('div', attrs={'data-target': 'doc'})
    download_id = []
    for content in parsed_html:
        download_id.append(content['data-id'])

    return dict(zip(doc_titles, download_id))

def load_dataframes(drive_dictionary):
    """
    Loads the data from the driven given in the dictionary to the data folder of the project.

    @param id_dictionary:
    @return:
    """
    for doc_key in drive_dictionary.keys():
        path = 'https://drive.google.com/uc?export=download&id=' + drive_dictionary[doc_key]
        df = pd.read_csv(path)
        df = transform(df=df)
        df.to_csv('../data/{}'.format(doc_key))


if __name__ == '__main__':
    drive_content = get_drive_content(drive_url='https://drive.google.com/drive/u/0/folders/1EuS-oOMSMH_0UE5bxKgAwExjFKxoM3tq')
    print('Collected Content from Drive: ', drive_content)
    time.sleep(2)
    load_dataframes(drive_dictionary=drive_content)
    print('Dataframes saved to Data Folder')
    time.sleep(2)