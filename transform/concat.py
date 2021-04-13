import os
import pandas as pd
import time

def concatenate_csv(path_2_write):
    """
    Concatenates all df with given lists.
    
    """
    df_paths = os.listdir('../data/')
    
    df = pd.DataFrame()

    for path in df_paths if '.csv' in path:
        df_ = pd.read_csv(path)
        df = pd.concat([df, df_], axis=0)

    df.to_csv(path_2_write)

                
def csv_remove():
    """
    """
    path_2_dir = '../data/'
    files = os.listdir(path_2_dir)
    
    for file in files:
        if file != 'tweets.csv':
            os.remove(path_2_dir+file)



if __name__ == '__main__':
    
    concatenate_csv(path_2_write='../data/tweets.csv')
    print(f'{time.ctime()} ---- Dataframes have been concatenated.')
    time.sleep(1)
    
    csv_remove()
    print(f'{time.ctime()} ---- CSV-Files removed.')
    time.sleep(2)
    
    os.system('../transform/read_transform.py')
