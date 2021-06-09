import pandas as pd
import networkx as nx
import sys
import time
sys.path.append('../streaming')
from transform.read_transform import read_transform

if __name__ == '__main__':
    data = read_transform(path_tweets='../data/TW.csv', path_retweets='../data/RT.csv',
                          join_method='concat',
                          hashtags_as_list=False, mentions_as_list=False)
    print('Dataframe loaded with shape: ', data.shape)
    time.sleep()

    # All mentions in a dict
    tmp = data[['mentions', 'user_screen_name']]
    tmp.loc[:, 'mentions'] = tmp.loc[:, 'mentions'].str.replace("'", "").str.split(', ')
    tmp = tmp.fillna(0)
    tmp = tmp.set_index('user_screen_name')
    mentions = tmp.to_dict()['mentions']
    time.sleep(1)

    # Extract all follower count in a dict
    tmp = data[['user_screen_name', 'followers_count']].set_index('user_screen_name')
    follower_counts = tmp.to_dict()['followers_count']
    time.sleep(1)

    # Extract all retweet counts in a dict
    tmp = data[['user_screen_name', 'retweet_count']].groupby('user_screen_name').mean()
    retweet_counts = tmp.to_dict()['retweet_count']
    time.sleep(1)

    # Add attribute activity
    tmp = data.drop_duplicates(subset=['tweet_id', 'user_screen_name'])['user_screen_name'].value_counts()
    user_activity = tmp.to_dict()
    time.sleep(1)

    print('Create Graph-File:')
    # Create Graph file
    G = nx.DiGraph()
    # Add nodes
    iteration = 1
    for key, mention in mentions.items():
        sys.stdout.flush()
        sys.stdout.write('\r---- {} of {} Nodes added ----'.format(iteration, len(mentions) + 1))
        G.add_node(key, followers_count=follower_counts[key], user_activity=user_activity[key],
                   retweet_counts=retweet_counts[key])
        if type(mentions) != 0:
            for m in mentions:
                G.add_node(m, followers_count=follower_counts[m], user_activity=user_activity[m],
                           retweet_counts=retweet_counts[m])

        iteration += 1

    # Add edges
    iteration = 1
    for key, val in mentions.items():
        sys.stdout.flush()
        sys.stdout.write('\r---- {} of {} Edges added ----'.format(iteration, len(mentions) + 1))
        if val != 0:
            for v in val:
                G.add_edge(key, v)
        iteration += 1
