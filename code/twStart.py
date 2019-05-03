
from twitter import Twitter, OAuth, oauth_dance, read_token_file
import os
import urllib.parse
import configparser

IN_DEBUG_MODE: bool = True

@property
def WhiteListUsers():
    return ['114742002', '123456789']

def DataFolder():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path + "/../data"

def ConfigFolder():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path + "/../config"

def hitTwitter():
    cfg = configparser.ConfigParser()
    cfg.read(ConfigFolder() + "/myTwitter.cfg")

    TW_ACCOUNT = cfg.get('auth', 'ACCOUNT')
    CONSUMER_KEY = cfg.get('auth', 'CONSUMER_KEY')
    CONSUMER_SECRET = cfg.get('auth', 'CONSUMER_SECRET')
    MY_TWITTER_CREDS = os.path.expanduser(ConfigFolder() + '/.tw_credentials_' + TW_ACCOUNT)

    if not os.path.exists(DataFolder()):
        os.makedirs(DataFolder())

    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("TW_App", 
                    CONSUMER_KEY, 
                    CONSUMER_SECRET,
                    MY_TWITTER_CREDS)


    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

    tw = Twitter(auth=OAuth(
                    oauth_token, 
                    oauth_secret, 
                    CONSUMER_KEY, 
                    CONSUMER_SECRET))
    
    return tw

def UserDetails(tw, uid):
    u = tw.users.show(user_id=uid)
    return u