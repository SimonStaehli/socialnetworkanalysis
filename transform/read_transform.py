import pandas as pd
import numpy as np


def transform(df, hashtags_as_list=False, mentions_as_list=False):
    """
    (pd.DataFrame) --> pd.DataFrame

    Transforms the Tweets Data.

    @param mentions_as_list: True if mentions should be a list in resulting dataframe else string
    @param hashtags_as_list: True if hashtags should be a list in resulting dataframe else string
    Attention: If this boolean parameters mentions_as_list and hashtags_as_list are set as true,

    @param df: pd.DataFrame(), which shall be transformed
    @return: pd.DataFrame()

    """
    # Drop Unnamed columns
    drop_cols = [col for col in df.columns if 'Unnamed' in col]
    df = df.drop(drop_cols, axis=1)

    # Drop duplicate Rows
    df = df.drop_duplicates(subset=['tweet_id', 'creation_date', 'user_id'])

    # Set pd datetime of date
    df['creation_date'] = pd.to_datetime(df['creation_date'])
    df['profile_created_at'] = pd.to_datetime(df['profile_created_at'])

    # If start of the Twitter post with RT then set to true
    # Add new column if it is retweet
    df['is_retweet'] = df['full_text'].str.contains(pat=r'^RT', regex=True)

    # Change the format of column mentions to a list
    df['mentions'] = np.where(df['mentions'] == '[]', np.nan, df['mentions'])
    if mentions_as_list:
        df['mentions'] = df['mentions'].str.strip('[]').str.split(', ')
    else:
        df['mentions'] = df['mentions'].str.strip('[]')

    # Change the column hashtags to nan when empty else to a list
    df['entities_hashtags'] = np.where(df['entities_hashtags'] == '[]', np.nan, df['entities_hashtags'])
    if hashtags_as_list:
        df['entities_hashtags'] = df['entities_hashtags'].str.findall(pat=r"'(\w+)'")
    else:
        df['entities_hashtags'] = df['entities_hashtags'].str.strip('[]')
        df['entities_hashtags'] = df['entities_hashtags'].str.replace("'", "")

    return df


def read_transform(path_tweets, path_retweets, join_method='concat',
                   hashtags_as_list=False, mentions_as_list=False):
    """
    (str, str) --> pd.DataFrame()

    This function reads data from the two dataframes tweet and retweets.

    @param mentions_as_list: True if mentions should be a list in resulting dataframe else string
    @param hashtags_as_list: True if hashtags should be a list in resulting dataframe else string
    @param path_tweets: specify path of tweets csv file to read
    @param path_retweets: specify path of retweets csv to read
    @param join_method: 'concat' or 'join'
    if concat: then dataframe gets concateanted over axis=0
    if join then dataframe will be left joined together
    @return: pandas dataframe

    """
    # Read Dataframes of Tweets and Retweets
    tweets = pd.read_csv(path_tweets)
    retweets = pd.read_csv(path_retweets)

    tweets = transform(df=tweets, hashtags_as_list=hashtags_as_list, mentions_as_list=mentions_as_list)
    retweets = transform(df=retweets, hashtags_as_list=hashtags_as_list, mentions_as_list=mentions_as_list)

    if join_method == 'concat':
        data = pd.concat([tweets, retweets],
                         axis=0
                         )
    elif join_method == 'join':
        data = pd.merge(left=tweets, right=retweets,
                        left_on='tweet_id', right_on='RT_of_ID',
                        how='left'
                        )
    else:
        data = (tweets, retweets)

    return data
