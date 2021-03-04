import tweepy
import time
import json
import yaml


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

    def __init__(self, auth, start_follower_name, follower_count_limit,
                 net_depth, extract_names_only=True,
                 print_collection_status=False):
        """
        :param auth: Authentication for Twitter API
        :param start_follower_name: Follower based as central node / Could also be a list of potential start followers.
        :param follower_count_limit: Limit for each user to obtain followers from. i.e. User has to 2 Mio. Followers
        then it will be skipped.
        :param net_depth: How much nodes from each follower the network should be expanded.
        (if every user has 500 follows -> 500^net_depth!!!)
        :param extract_names_only: if true extracts just the follower names.

        """
        self.auth = auth
        self.api = tweepy.API(auth_handler=auth,
                              wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True,
                              compression=True
                              )
        try:
            self.api.verify_credentials()  # accounts method
            print("Authentication OK")
        except:
            print("Error during authentication")

        self.start_follower = start_follower_name
        self.follower_count_limit = follower_count_limit
        self.follower_results = {}
        self.net_depth = net_depth
        self.extract_names_only = extract_names_only
        self.print_collection_status = print_collection_status

    def create_network(self):
        """
        Collects a network of followers for a given user. Pay attention to the RateLimiting of the Twitter API. It will
        take 15 mins to recover.

        Note: Some users a protected and no followers can be collected from them. -> End node
        """
        follower_counter = 0

        if type(self.start_follower) != list:
            followers_list = [self.start_follower]
        else:
            followers_list = self.start_follower.copy()

        for depth in range(self.net_depth):
            new_followers_list = []
            print(f'Depth: {depth}')

            for follower in followers_list:
                # Performs the action only if follower data not present and smaller than given follower count limit
                if (follower not in list(self.follower_results.keys())) and (self.api.get_user(follower).followers_count <= self.follower_count_limit):
                    try:
                        results = self._get_followers(user_name=follower, extract_names_only=self.extract_names_only)
                        self.follower_results[follower] = results

                        if self.print_collection_status:
                            print(f'Followers Added for @{follower}...')
                            follower_counter += len(results)
                            print(f'{follower_counter} Followers collected.')

                        # Generate new list of followers
                        for flwr in self.follower_results[follower]:
                            new_followers_list.append(flwr)
                    except:
                        print(f'*** Could not perform action for this Follower. @{follower} ***')
                else:
                    pass
            # New generated list for the next iteration
            followers_list = new_followers_list.copy()

        self._write_json()
        print('JSON was written to Working Directory.')

    def _get_followers(self, user_name, extract_names_only=True):
        """
        Get a list of all followers of a twitter account

        :param user_name: twitter username without '@' symbol
        :return: list of usernames without '@' symbol
        """
        followers = []

        for page in tweepy.Cursor(self.api.followers, screen_name=user_name, wait_on_rate_limit=True, count=200).pages():
            try:
                followers.extend(page)
            except tweepy.TweepError as e:
                print("Going to sleep:", e)
                time.sleep(60*5)

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

        self.follower_results = {}


if __name__ == '__main__':
    with open('creds.yaml', 'r') as yaml_file:
        creds = yaml.load(yaml_file, Loader=yaml.FullLoader)

    # Authorize to access the Twitter API
    auth = tweepy.OAuthHandler(consumer_key=creds['API_key'],
                               consumer_secret=creds['API_secret_keys'])
    auth.set_access_token(key=creds['Access_token'],
                          secret=creds['Access_token_secret'])

    twitter_network = TwitterFollowersNetwork(auth=auth,
                                              start_follower_name=input('Input Start Follower: '),
                                              follower_count_limit=int(input('Type follower limit for each User: ')),
                                              net_depth=int(input('Input Net Depth of the Followers Network: ')),
                                              print_collection_status=True
                                              )
    twitter_network.create_network()
