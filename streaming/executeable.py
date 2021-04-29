from collect.tweets import HashForATweet
import yaml
import tweepy
import time
import subprocess

search_word = 'vegan_burger'

if __name__ == '__main__':
    with open('creds.yaml', 'r') as yaml_file:
        creds = yaml.load(yaml_file, Loader=yaml.FullLoader)

    # Authorize to access the Twitter API
    auth = tweepy.OAuthHandler(consumer_key=creds['API_key'],
                               consumer_secret=creds['API_secret_keys'])
    auth.set_access_token(key=creds['Access_token'],
                          secret=creds['Access_token_secret'])

    since_id = None
    while True:
        try:
            hashfortweet = HashForATweet(
                authentication=auth,
                search_key=search_word,
                amount_tweets=200,
                search_results='recent',
                language='en',
                since_id=since_id
            )
            hashfortweet.collect_tweets()
            hashfortweet.write_tweets_csv()
            since_id = hashfortweet.since_id

            subprocess.run(['concat.py'], shell=True, cwd='../transform')

        except:
            raise Exception('Iteration failed. Proceeding with next Iteration.')

        finally:
            sleep_for = 1
            print(f'Sleep for {sleep_for} minute...')
            time.sleep(sleep_for*60)

