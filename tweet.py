import tweepy
import keys
from datetime import date

def tweet(top_20_hitters):
    tweet = ""
    tweet += "Home Run Predictions for " + str(date.today().strftime("%B %d, %Y"))+'\n\n'

    for i in range(5):
        tweet += str(i+1) + ". " + top_20_hitters[i][0] + " (" + top_20_hitters[i][2] + "): " + str(round(top_20_hitters[i][1],1))
        tweet += '\n'

    client = tweepy.Client(consumer_key=keys.api_key,
                    consumer_secret=keys.api_secret,
                    access_token=keys.access_token,
                    access_token_secret=keys.access_token_secret)
    
    response = client.create_tweet(text=tweet)
    print('Tweeted!')
    return