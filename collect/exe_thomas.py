from tweets import HashForATweet
import yaml
import tweepy
import sys
import json

with open('hashtags.json', 'r') as json_file:
    json_file = json.load(json_file)

search_words = json_file['Thomas']

def printProgressBar(i,max,postText):
    n_bar =30 #size of progress bar
    j= i/max
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {postText} ")
    sys.stdout.flush()

if __name__ == '__main__':
    with open('creds.yaml', 'r') as yaml_file:
        creds = yaml.load(yaml_file, Loader=yaml.FullLoader)

    # Authorize to access the Twitter API
    auth = tweepy.OAuthHandler(consumer_key=creds['API_key'],
                               consumer_secret=creds['API_secret_keys'])
    auth.set_access_token(key=creds['Access_token'],
                          secret=creds['Access_token_secret'])

    progress_counter = 0
    for word in search_words:
        printProgressBar(
            i=progress_counter,
            max=len(search_words),
            postText=f'Search Word: {word}'
        )
        hashfortweet = HashForATweet(
            authentication=auth,
            search_key=word,
            amount_tweets=1000,
            upper_retweet_limit=500,
            lower_retweet_limit=1,
            search_results='mix',
            language='en'
        )
        hashfortweet.collect_tweets()
        hashfortweet.write_tweets_csv()

        hashfortweet.collect_retweets()
        hashfortweet.write_retweets_csv()

        progress_counter += 1
