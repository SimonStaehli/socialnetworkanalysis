import tweepy
import time
import yaml
import pandas as pd
import datetime as dt

class HashForATweet:
    """
    This Class is meant to be for the collection of Twitter Tweets and Retweets for a provided search key.
    """

    def __init__(self, authentication,
                 search_key, amount_tweets,
                 retweet_limit, search_results='mix', language='en'):
        """
        :param authentication:
        Authentication Object of TwitterAPI

        :param search_key:
        Keyword to search Tweets for on Twitter

        :param amount_tweets:
        Amount of Tweets to be extracted from Twitter

        :param retweet_limit:
        A limit of how much Retweets for a Tweet to be collected

        :param search_results:
        Refering to Twitter options for the Tweets: popular / mix / recent

        :param language:
        Language for the Twitter Tweets.
        """

        self.auth = authentication
        self.api = tweepy.API(auth_handler=authentication,
                              wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True,
                              compression=True
                              )
        try:
            self.api.verify_credentials()  # accounts method
            print("-- Authentication OK --")
        except:
            print("Error during authentication")

        self.search_key = search_key
        self.language = language
        self.amount_tweets = amount_tweets
        self.retweet_limit = retweet_limit
        self.search_results = search_results
        self.tweets = []
        self.retweets = {}

    def collect_tweets(self):
        """
        Collects Tweets from the API with given Search Keys

        :return A list of Tweets
        """
        for status in tweepy.Cursor(self.api.search, q=self.search_key, lang=self.language, tweet_mode='extended',
                                    result_type=self.search_results, wait_on_rate_limit=True).items(self.amount_tweets):
            try:
                self.tweets.append(status._json)
            except tweepy.TweepError as e:
                print("Going to sleep:", e)
                time.sleep(60 * 5)

    def collect_retweets(self):
        """
        Collects Retweets to given Tweets. The given Tweets must be collected before this method is called.

        :return: A Dictionary of Retweets for a certain Tweet_id
        """
        if len(self.tweets) > 0:
            for tweet in self.tweets:
                if tweet['retweet_count'] <= self.retweet_limit:
                    tweet_id = tweet['id']
                    self.retweets[tweet_id] = []
                    for retweet in self.api.retweets(tweet_id):
                        self.retweets[tweet_id].append(retweet._json)
                else:
                    pass
        else:
            print('List of Tweets to get Retweets from is empty. Run collect_tweets() first.')

    def write_tweets_csv(self):
        """
        Writes Twitter Tweets Data to a csv-file.

        :return: Written CSV to working dir
        """
        # Create Empty Dataframe
        df = pd.DataFrame(
            columns=[
                'tweet_id', 'creation_date', 'full_text', 'mentions', 'entities_hashtags',
                'user_name', 'user_screen_name', 'user_id', 'location', 'description',
                'protected', 'followers_count', 'friends_count', 'profile_created_at',
                'favourites_count', 'statuses_count', 'retweet_count', 'favourite_count'
            ]
        )
        for tweet in self.tweets:
            df = df.append(
                {
                    'tweet_id': tweet['id'], 'creation_date': tweet['created_at'],
                    'full_text': tweet['full_text'],
                    'mentions': [', '.join([user['screen_name']]) for user in tweet['entities']['user_mentions']],
                    'entities_hashtags': tweet['entities']['hashtags'], 'user_id': tweet['user']['id'],
                    'user_name': tweet['user']['name'], 'user_screen_name': tweet['user']['screen_name'],
                    'location': tweet['user']['location'], 'description': tweet['user']['description'],
                    'protected': tweet['user']['protected'], 'followers_count': tweet['user']['followers_count'],
                    'friends_count': tweet['user']['friends_count'], 'profile_created_at': tweet['user']['created_at'],
                    'favourites_count': tweet['user']['favourites_count'],
                    'statuses_count': tweet['user']['statuses_count'],
                    'retweet_count': tweet["retweet_count"], 'favourite_count': tweet["favorite_count"]

                },
                ignore_index=True
            )
        df.to_csv(path_or_buf=f'../data/{self.search_key.replace(" ", "_")}_tweet_{str(dt.datetime.today().date())}')

    def write_retweets_csv(self, path):
        """
        Writes Twitter Tweets Data to a csv-file.

        :return: Written CSV to working dir
        """
        # Create Empty Dataframe
        df = pd.DataFrame(
            columns=[
                'tweet_id', 'creation_date', 'full_text', 'mentions', 'entities_hashtags',
                'user_name', 'user_screen_name', 'user_id', 'location', 'description',
                'protected', 'followers_count', 'friends_count', 'profile_created_at',
                'favourites_count', 'statuses_count', 'retweet_count', 'favourite_count',
                "RT_of_ID"
            ]
        )
        for key in self.retweets.keys():
            for tweet in self.retweets[key]:
                df = df.append(
                    {
                        'tweet_id': tweet['id'], 'creation_date': tweet['created_at'],
                        'full_text': tweet['text'],
                        'mentions': [', '.join([user['screen_name']]) for user in tweet['entities']['user_mentions']],
                        'entities_hashtags': tweet['entities']['hashtags'], 'user_id': tweet['user']['id'],
                        'user_name': tweet['user']['name'], 'user_screen_name': tweet['user']['screen_name'],
                        'location': tweet['user']['location'], 'description': tweet['user']['description'],
                        'protected': tweet['user']['protected'], 'followers_count': tweet['user']['followers_count'],
                        'friends_count': tweet['user']['friends_count'],
                        'profile_created_at': tweet['user']['created_at'],
                        'favourites_count': tweet['user']['favourites_count'],
                        'statuses_count': tweet['user']['statuses_count'],
                        'retweet_count': tweet["retweet_count"], 'favourite_count': tweet["favorite_count"],
                        "RT_of_ID": tweet["retweeted_status"]["id"],
                    },
                    ignore_index=True
                )

        df.to_csv(path_or_buf=f'../data/{self.search_key.replace(" ", "_")}_retweets_{str(dt.datetime.today().date())}')


if __name__ == '__main__':
    with open('creds.yaml', 'r') as yaml_file:
        creds = yaml.load(yaml_file, Loader=yaml.FullLoader)

    # Authorize to access the Twitter API
    auth = tweepy.OAuthHandler(consumer_key=creds['API_key'],
                               consumer_secret=creds['API_secret_keys'])
    auth.set_access_token(key=creds['Access_token'],
                          secret=creds['Access_token_secret'])

    hash_for_tweet = HashForATweet(authentication=auth,
                                   search_key=input('Type in Search Key: '),
                                   amount_tweets=int(input("Type in amount of Tweets: ")),
                                   retweet_limit=int(input("Type limit of Retweets : ")),
                                   search_results=input('Search Criterion (mix/popular/recent): '),
                                   language='en')

    hash_for_tweet.collect_tweets()
    print(f'{len(hash_for_tweet.tweets)} Tweets collected...')

    hash_for_tweet.collect_retweets()
    print(
        f'{sum([len(hash_for_tweet.retweets[key]) for key in hash_for_tweet.retweets.keys()])} Retweets collected....')
    hash_for_tweet.write_tweets_csv()
    hash_for_tweet.write_retweets_csv()
