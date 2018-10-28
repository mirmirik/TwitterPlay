'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, takipçi ve takip edilenler listesini almak için yazılmış deneme / sandbox kodu.
myTwitter.cfg dosyası içine ilgili değerleri ekleyip, komut satırından "python twPlay.py" yazarak çalıştırılabilir.

Konfigürasyon dosyası değerleri:
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olacan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olacan CONSUMER SECRET>

    [runtime]
    FOLLOWER_FILE = Takipçilerin bilgilerinin yazılacağı text dosya ismi. DATA dizini içinde yaratılır. Tab delimeted dosya oluşturur.
    FOLLOWING_FILE = Takip edilenlerin bilgilerinin yazılacağı text dosya ismi. DATA dizini içinde yaratılır. Tab delimeted dosya oluşturur.

IN_DEBUG_MODE = True ise, 
    tüm ilgili kullanıcı nesnesine ait bilgiler "raw_data.json" isimli dosyaya da JSON formatında yazılır. Buradaki alanlar incelenip göre
    kullanıcılara ait farklı bilgilere de erişim sağlanabilir.

Twitter API'ye erişim sağlayan wrapper library:
    https://github.com/sixohsix/twitter

Twitter User Object detayları:
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

Geliştiriciler için kullanıcı ve hesap bilgilerinin kullanımı :

    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview
'''
from twitter import Twitter, OAuth, oauth_dance, read_token_file
import os
import json
from datetime import datetime
import urllib.parse
import configparser

IN_DEBUG_MODE: bool = True
GET_FOLLOWERS: bool = False


cfg = configparser.ConfigParser()
cfg.read("myTwitter.cfg")

TW_ACCOUNT = cfg.get('auth', 'ACCOUNT')
CONSUMER_KEY = cfg.get('auth', 'CONSUMER_KEY')
CONSUMER_SECRET = cfg.get('auth', 'CONSUMER_SECRET')
MY_TWITTER_CREDS = os.path.expanduser('.tw_credentials_' + TW_ACCOUNT)

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

activeCursor = -1

fileName = "data/" + cfg.get('runtime', 'FOLLOWER_FILE') if GET_FOLLOWERS else "data/" + cfg.get('runtime', 'FOLLOWING_FILE')

fl = open("data/raw_data.json", "w+")
fn = open(fileName, "w+")

print("{:25s} {:25s} {:25s} {:25s} {:25s}".format(
    "Screen Name", "Name", "ID", "Last Interaction", "Protected"))
print("---------------------------------------------------------------------------------------------------------------------------------------------")

fn.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format("screen_name",
                                                "name",
                                                "id_str",
                                                "followers_count", 
                                                "friends_count",
                                                "last_interaction",
                                                "protected") + "\n")

while activeCursor != 0:

    f = tw.followers.list(cursor=activeCursor, count=200) if GET_FOLLOWERS else tw.friends.list(cursor=activeCursor, count=200)

    _lastInteraction = ""
    for usr in f["users"]:
        try:
            if (usr["status"]):
                # TW standart tarih formatı: Sat Aug 11 12:51:00 +0000 2018
                _tempDate = usr["status"]["created_at"]
                dtObj = datetime.strptime(_tempDate, '%a %b %d %H:%M:%S %z %Y')
                _lastInteraction = "{2}{1}{0}".format(
                    str(dtObj.day).zfill(2), 
                    str(dtObj.month).zfill(2), 
                    str(dtObj.year))

                # En son 2018 / 6. aydan önce tweet atmışları takipten çıkaralım.
                # if (dtObj.year = 2018 && dtObj.month < 6 ):
                #    tw.friendships.destroy(user_id=usr["id_str"])

        except KeyError as ke:
            _lastInteraction = "Not found"

        print("{:25s} {:25s} {:25s} {:25s}".format(
            usr["screen_name"], usr["name"], usr["id_str"], _lastInteraction))
        
        fn.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(
            usr["screen_name"], 
            usr["name"], 
            usr["id_str"], 
            usr["followers_count"], 
            usr["friends_count"], 
            _lastInteraction, 
            usr["protected"]) + "\n")

    activeCursor = f["next_cursor"]
    if IN_DEBUG_MODE:
        jsDump = json.dumps(f, indent=4, sort_keys=False)
        fl.write(jsDump)

fl.close()
fn.close()