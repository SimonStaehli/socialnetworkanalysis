from tweets import HashForATweet
import yaml
import tweepy
import sys
import os

search_words = 'crypto'

if __name__ == '__main__':
    with open('creds.yaml', 'r') as yaml_file:
        creds = yaml.load(yaml_file, Loader=yaml.FullLoader)

    # Authorize to access the Twitter API
    auth = tweepy.OAuthHandler(consumer_key=creds['API_key'],
                               consumer_secret=creds['API_secret_keys'])
    auth.set_access_token(key=creds['Access_token'],
                          secret=creds['Access_token_secret'])
    since_id = None
    
    # while True:
    for i in range(2):

        hashfortweet = HashForATweet(
            authentication=auth,
            search_key=word,
            amount_tweets=1000,
            search_results='recent',
            language='en',
            max_id=since_id
        )
        hashfortweet.collect_tweets()
        hashfortweet.write_tweets_csv()
        since_id = hashfortweet.id_max

    os.system('../transform/concat.py')
    time.sleep(10)

