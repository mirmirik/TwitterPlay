
from twitter import Twitter, OAuth, oauth_dance, read_token_file
import os
from datetime import datetime
import urllib.parse
import configparser
import requests

IN_DEBUG_MODE: bool = True

WHITE_LIST_USERS = ['114742002', '123456789']
BLACK_LIST_USERS = ['123456789']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = BASE_DIR + "/data"
CONFIG_FOLDER = BASE_DIR + "/config"

def splitArray(arraySize, maxRequest):
    modulusCalculation = arraySize % maxRequest
    fixedLoop = arraySize // maxRequest
    return modulusCalculation, fixedLoop

def check_internet():
    url='http://api.twitter.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

def hitTwitter():
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FOLDER + "/myTwitter.cfg")

    TW_ACCOUNT = cfg.get('auth', 'ACCOUNT')
    CONSUMER_KEY = cfg.get('auth', 'CONSUMER_KEY')
    CONSUMER_SECRET = cfg.get('auth', 'CONSUMER_SECRET')
    MY_TWITTER_CREDS = os.path.expanduser(CONFIG_FOLDER + '/.tw_credentials_' + TW_ACCOUNT)

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("TW_App", 
                    CONSUMER_KEY, 
                    CONSUMER_SECRET,
                    MY_TWITTER_CREDS)


    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
    if (check_internet()):
        tw = Twitter(auth=OAuth(
                        oauth_token, 
                        oauth_secret, 
                        CONSUMER_KEY, 
                        CONSUMER_SECRET))
    else:
        raise urllib.error.URLError("No internet connection")

    return tw

def UserDetails(tw, uid):
    u = tw.users.show(user_id=uid)
    return u

def BUM(tw, user, userId, action):
    """ Block, Unfollow or Mute function based on the parameters. If user is in the WhiteList, then returns without
    doing anything.\n
    tw:     Twitter object that will be used in API calls,\n
    user:   UserId to be processed,\n
    action: 'B' for blocking, 'U' to unfollow and 'M' for muting.
    """

    if (user in WHITE_LIST_USERS):
        return

    if(action == "B"):
        print("Blocked: {0}".format(user))
        # TODO: Uncomment the code below
        # tw.blocks.create(user_id=userId, skip_status=1, include_entities=False)
        return
    elif (action == "M"):
        print("Muted: {0}".format(user))
        # TODO: Uncomment the code below
        # tw.users.mutes(user_id=userId)
        return
    elif(action == "U"):
        print("Unfollowed: {0}".format(user))
        # TODO: Uncomment the code below
        # tw.friendships.destroy(user_id=userId)
    return

def sendMessage(tw, toUser, sendThisMessage):
    tw.direct_messages.events.new(
    _json={
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": toUser},
                "message_data": {
                    "text": sendThisMessage}}}})


def FormatTwitterDate(twDate, rettype='S'):
    '''TW standart tarih formatı: Sat Aug 19 12:51:00 +0000 2019

    - Dönüş (str):
        20190819
    '''

    ret = datetime.today().strftime('%Y%m%d')
    try:
        tempDate = datetime.strptime(twDate, '%a %b %d %H:%M:%S %z %Y')
        ret = "{2}{1}{0}".format(
                        str(tempDate.day).zfill(2), 
                        str(tempDate.month).zfill(2), 
                        str(tempDate.year))
    except:
        pass

    return datetime.strptime(ret, '%Y%m%d') if rettype == 'D' else ret