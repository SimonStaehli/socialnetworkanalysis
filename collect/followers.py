import tweepy
import time
import json


class TwitterFollowersNetwork:
    """
    This class collects data from Twitter by using the start_follower_name as start. The network will be expanded
    according to given parameter net_depth.

    Network with Net_depth of 2 for a person with 2 Followers. And 2 followers of followers (followers^net_depth!):

                                    start_follower_name
                                     |              |
                                     F1            F2
                                  |     |        |    |
                                F11     F12     F21  F22

    """
    def __init__(self, auth, start_follower_name,
                 net_depth, extract_names_only=True):
        """
        :param auth: Authentication for Twitter API
        :param start_follower_name: Follower based as central node / Could also be a list of potential start followers.
        :param net_depth: How much nodes from each follower the network should be expanded.
        (if every user has 500 follows -> 500^net_depth!!!)
        :param extract_names_only: if true extracts just the follower names.

        """
        self.auth = auth
        self.api = tweepy.API(auth_handler=auth,
                              wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True,
                              compression=True)
        self.start_follower = start_follower_name
        self.follower_results = {}
        self.net_depth = net_depth
        self.extract_names_only = extract_names_only

    def create_network(self):
        """
        Collects a network of followers for a given user. Pay attention to the RateLimiting of the Twitter API. It will
        take 15 mins to recover.

        Note: Some users a protected and no followers can be collected from them. -> End node
        """
        if type(self.start_follower) != list:
            followers_list = [self.start_follower]
        else:
            followers_list = self.start_follower.copy()

        for depth in range(self.net_depth):
            new_followers_list = []

            for follower in followers_list:
                if follower not in list(self.follower_results.keys()):
                    try:
                        results = self._get_followers(user_name=follower, extract_names_only=self.extract_names_only)
                        self.follower_results[follower] = results
                        print(f'Followers Added for @{follower}...')

                        # Generate new list of followers
                        for flwr in self.follower_results[follower]:
                            new_followers_list.append(flwr)
                    except:
                        print(f'*** Could not perform action for this Follower. @{follower} ***')
                else:
                    pass
            # New generated list for the next iteration
            followers_list = new_followers_list

        self._write_json()
        print('JSON was written to Working Directory.')

    def _get_followers(self, user_name, extract_names_only=True):
        """
        Get a list of all followers of a twitter account

        :param user_name: twitter username without '@' symbol
        :return: list of usernames without '@' symbol
        """
        api = tweepy.API(self.auth)
        followers = []
        for page in tweepy.Cursor(api.followers, screen_name=user_name, wait_on_rate_limit=True, count=200).pages():
            try:
                followers.extend(page)
            except tweepy.TweepError as e:
                print("Going to sleep:", e)
                time.sleep(60)

        if extract_names_only:
            followers = [follower._json['screen_name'] for follower in followers]

        return followers
    
    def _write_json(self):
        """
        Writes Twitter Data to a JSON-file.

        :return: Json saved to working dir
        """
        with open(f'Twitter_Data_{self.start_follower}_depth{self.net_depth}', 'w') as json_file:
            json.dump(self.follower_results, json_file)


