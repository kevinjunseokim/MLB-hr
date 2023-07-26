import os
import tweepy
from datetime import date

consumer_key = os.environ.get('API_KEY')
consumer_secret = os.environ.get('API_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')


def tweet(top_20_hitters):

    team_hashtag = {
        "ARI":'ArizonaBorn',
        "ATL":'ForTheA',
        "BAL":'Birdland',
        "BOS":'DirtyWater',
        "CHW":'WhiteSox',
        "CHC":'NextStartsHere',
        "CIN":'ATOBTTR',
        "CLE":'ForTheLand',
        "COL":'Rockies',
        "DET":'RepDetroit',
        "HOU":'Ready2Reign',
        "KCR":'WelcomeToTheCity',
        "LAA":'GoHalos',
        "LAD":'HereToPlay',
        "MIA":'MakeItMiami',
        "MIL":'ThisIsMyCrew',
        "MIN":'MNTwins',
        "NYY":'RepBX',
        "NYM":'LGM',
        "OAK":'Athletics',
        "PHI":'RingTheBell',
        "PIT":'LetsGoBucs',
        "SDP":'BringTheGold',
        "SFG":'SFGiants',
        "SEA":'SeaUsRise',
        "STL":'STLCards',
        "TBR":'RaysUp',
        "TEX":'StraightUpTX',
        "TOR":'NextLevel',
        "WSN":'NATITUDE'
    }

    tweet = ""
    tweet += "Home Run Predictions for " + str(date.today().strftime("%B %d, %Y"))+'\n\n'

    hashtag = set()

    for i in range(5):
        tweet += str(i+1) + ". " + top_20_hitters[i][0] + " (" + top_20_hitters[i][2] + "): " + str(round(top_20_hitters[i][1],1))
        tweet += '\n'
        hashtag.add(team_hashtag[top_20_hitters[i][2]])

    for team in hashtag:
        tweet += '\n#'+team

    tweet += '\n\n#MLBTwitter #MLBPicks #MLBBets'

    client = tweepy.Client(consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret)
    
    response = client.create_tweet(text=tweet)
    print('Tweeted!')
    return
