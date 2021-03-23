from tweets import HashForATweet
import yaml
import tweepy
import sys

search_words = '#vegan #plantbased #veganfood #vegetarian #healthyfood #crueltyfree #food #organic #glutenfree #healthy #veganlife #healthylifestyle #govegan #foodie #foodporn #vegansofig #veganrecipes #love #veganism #instafood #vegano #natural #whatveganseat #fitness #veganfoodshare #health #yummy #dairyfree #homemade #bhfyp'
search_words = search_words.split(sep='#')
search_words = [word.strip() for word in search_words][1:]

def printProgressBar(i,max,postText):
    n_bar =10 #size of progress bar
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
            amount_tweets=250,
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
