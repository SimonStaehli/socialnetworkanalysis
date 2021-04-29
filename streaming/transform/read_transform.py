import pandas as pd
import datetime as dt
import time
import subprocess


def transform(df):
    """
    (pd.DataFrame) --> pd.DataFrame

    Transforms the Tweets Data.

    @param df: pd.DataFrame(), which shall be transformed
    @return: pd.DataFrame()

    """
    # Drop Unnamed columns
    drop_cols = [col for col in df.columns if 'Unnamed' in col]
    df = df.drop(drop_cols, axis=1)

    # Drop duplicate Rows
    df = df.drop_duplicates(subset=['tweet_id'])

    # Set pd datetime of date
    #df['creation_date'] = pd.to_datetime(df['creation_date'])

    # If start of the Twitter post with RT then set to true
    # Add new column if it is retweet
    df['is_retweet'] = df['full_text'].str.contains(pat=r'^RT', regex=True)

    return df


if __name__ == '__main__':
    tweets = pd.read_csv(filepath_or_buffer='../data/tweets.csv',
                         dtype={'tweet_id': 'int', 'creation_date': 'datetime',
                                'full_text': 'string',
                                'user_screen_name': 'string',
                                'followers_count': 'int',
                                'friends_count': 'int',
                                'retweet_count': 'int', 'favourite_count': 'int'}
                         )
    tweets = transform(df=tweets)

    tweets.to_csv('../data/tweets.csv')

    print(f'{time.ctime()} ---- Transformation of data folder Done.')
    print(f'{tweets.shape[0]} distinct Tweets have been collected.')
    time.sleep(2)

    #subprocess.run(['gdriveupload.py'], shell=True, cwd='../integrate')

