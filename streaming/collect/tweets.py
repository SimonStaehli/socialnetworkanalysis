import tweepy
import time
import pandas as pd
import datetime as dt


class HashForATweet:
    """
    This Class is meant to be for the collection of Twitter Tweets and Retweets for a provided search key.
    """

    def __init__(self, authentication,
                 search_key, amount_tweets,
                 search_results='recent', language='en', since_id=None):
        """
        :param authentication:
        Authentication Object of TwitterAPI

        :param search_key:
        Keyword to search Tweets for on Twitter

        :param amount_tweets:
        Amount of Tweets to be extracted from Twitter

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

        self.search_key = search_key
        self.language = language
        self.amount_tweets = amount_tweets
        self.search_results = search_results
        
        self.tweets = []
        self.since_id = since_id

    def collect_tweets(self):
        """
        Collects Tweets from the API with given Search Keys

        :return A list of Tweets
        """
        for status in tweepy.Cursor(self.api.search, q=self.search_key, lang=self.language, tweet_mode='extended',
                                    result_type=self.search_results, wait_on_rate_limit=True, 
                                    since_id=self.since_id).items(self.amount_tweets):
            try:
                self.tweets.append(status._json)
                
            except tweepy.TweepError as e:
                print("Going to sleep:", e)
                time.sleep(60 * 5)
                
            self.since_id = max([tweet['id'] for tweet in self.tweets])

        return self

    def write_tweets_csv(self):
        """
        Writes Twitter Tweets Data to a csv-file.

        :return: Written CSV to working dir
        """
        # Create Empty Dataframe
        df = pd.DataFrame(
            columns=[
                'tweet_id', 'creation_date', 
                'full_text',
                'user_screen_name', 
                'followers_count', 
                'friends_count',
                'retweet_count', 'favourite_count'
            ]
        )
        for tweet in self.tweets:
            df = df.append(
                {
                    'tweet_id': tweet['id'], 'creation_date': tweet['created_at'],
                    'full_text': tweet['full_text'],
                    'user_screen_name': tweet['user']['screen_name'],
                    'followers_count': tweet['user']['followers_count'],
                    'friends_count': tweet['user']['friends_count'], 
                    'retweet_count': tweet["retweet_count"], 'favourite_count': tweet["favorite_count"]

                },
                ignore_index=True
            )
        df.to_csv(path_or_buf=f'../data/{dt.datetime.now().strftime(format="%y-%m-%d_%H%M")}_{self.search_key}.csv')