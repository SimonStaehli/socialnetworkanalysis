import os
import pandas as pd
import time
import datetime as dt
import subprocess

def concatenate_csv(path_2_write):
    """
    Concatenates all df with given lists.
    """
    path_to_data = '../data/'
    df_paths = os.listdir(path_to_data)
    
    df = pd.DataFrame()

    for path in df_paths:
        if '.csv' in path:
            df_ = pd.read_csv(filepath_or_buffer=path_to_data + path,
                              dtype={'tweet_id': 'int', 'creation_date': 'datetime',
                                     'full_text': 'string',
                                     'user_screen_name': 'string',
                                     'followers_count': 'int',
                                     'friends_count': 'int',
                                     'retweet_count': 'int', 'favourite_count': 'int'}
                              )
            df = pd.concat([df, df_], axis=0)

    df.to_csv(path_2_write)

                
def csv_remove():
    """
    """
    path_2_dir = '../data/'
    files = os.listdir(path_2_dir)

    try:
        for file in files:
            if file != 'tweets.csv':
                os.remove(path_2_dir+file)
    except:
        print('File not Found in Folder.')


if __name__ == '__main__':
    concatenate_csv(path_2_write='../data/tweets.csv')
    print(f'{time.ctime()} ---- Dataframes have been concatenated.')
    time.sleep(1)
    
    csv_remove()
    print(f'{time.ctime()} ---- CSV-Files removed.')
    time.sleep(2)

    subprocess.run(['read_transform.py'], shell=True)

