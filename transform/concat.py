import os
import pandas as pd
import time

def get_file_paths(path_to_dir='../data'):
    """
    Returns all file paths with prefix tw or rt in data folder

    @param path_to_dir:
    @return: names of tweets csv, names of retweet csv
    """
    os.chdir(path_to_dir)
    file_names = os.listdir()

    tweet_names = [i for i in file_names if i[:2] == 'TW']
    retweet_names = [i for i in file_names if i[:2] == 'RT']

    return tweet_names, retweet_names

def concatenate_csv(df_paths, path_2_write):
    """
    Concatenates all df with given lists.
    
    tweet_names = list of filenames of tweets
    retweet_names = list of filenames of retweets
    """

    df = pd.DataFrame()

    for path in df_paths:
        df_ = pd.read_csv(path)
        df = pd.concat([df, df_], axis=0)

    df.to_csv(path_2_write)

def archive_csv_objects(file_names):
    """
    Archives all exisiting file names in folder archived.

    @param file_names file names in data folder
    @return: None
    """
    os.chdir('../data')

    if 'archived' not in os.listdir():
        os.mkdir('archived')

    os.chdir('archived')
    archived_files = os.listdir()
    os.chdir('..')

    for file in file_names:
        if file not in ['RT.csv', 'TW.csv'] and '.csv' in file:
            print(file in archived_files)
            try:
                rename_path = './archived/' + file
                os.rename(file, rename_path)
            except:
                rename_path = './archived/' + file.split('.')[0] + '_1.' + file.split('.')[-1]
                os.rename(file, rename_path)


if __name__ == '__main__':

    tweet_names, retweet_names = get_file_paths()
    print('File paths in data folder collected.')
    time.sleep(1)
    
    #concatenate_csv(df_paths=tweet_names, path_2_write='../data/TW.csv')
    #concatenate_csv(df_paths=retweet_names, path_2_write='../data/RT.csv')
    print('Dataframes have been concatenated.')
    time.sleep(1)

    archive_csv_objects(file_names=tweet_names)
    archive_csv_objects(file_names=retweet_names)
    print('CSV-Files archived.')
    time.sleep(1)
