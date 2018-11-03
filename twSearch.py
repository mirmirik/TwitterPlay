'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, dış parametrelere göre tweeter içinde arama yapmak için yazılmış deneme / sandbox kodu.
myTwitter.cfg dosyası içine ilgili değerleri ekleyip, komut satırından "python twSearch.py -s <kelime>" yazarak çalıştırılabilir.

Parametreler:
    -s, --search    : Arama yapılacak text
    -r, --replyTo   : <kaldırılacak>, bir tweet'e cevap verilecekse, o tweet'in ID'si
    -t, --text      : <kaldırılacak>, Tweet reply olacaksa, verilecn cevap text'i.

Konfigürasyon dosyası değerleri:
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olacan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olacan CONSUMER SECRET>

Twitter API'ye erişim sağlayan wrapper library:
    https://github.com/sixohsix/twitter

Twitter Search detayları:
    https://developer.twitter.com/en/docs/tweets/search/overview
'''

import argparse
import sys
from twitter import Twitter, OAuth, oauth_dance, read_token_file
import os
import json
from datetime import datetime
import urllib.parse
import configparser

IN_DEBUG_MODE: bool = True
GET_FOLLOWERS: bool = True

cfg = configparser.ConfigParser()
cfg.read("myTwitter.cfg")

TW_ACCOUNT = cfg.get('auth', 'ACCOUNT')
CONSUMER_KEY = cfg.get('auth', 'CONSUMER_KEY')
CONSUMER_SECRET = cfg.get('auth', 'CONSUMER_SECRET')

SEARCH_RESULTS_FILE = "data/search_" + datetime.today().strftime('%Y%m%d') + ".txt"

MY_TWITTER_CREDS = os.path.expanduser('.tw_credentials_' + TW_ACCOUNT)

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("TW_App", 
                CONSUMER_KEY, 
                CONSUMER_SECRET,
                MY_TWITTER_CREDS)

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)


# def replyto_tweet(replyto, tweettext):
#     """ID'si verilen tweet'e tweettext parametresi ile verilen yazıyı 'reply' olarak ekler.

#     Parametreler:
#         - replyto -- Cevap verilecek tweet'in ID'si
#         - tweettext -- Verilecek cevap yazısız
#     """
#     tw = Twitter(auth=OAuth(
#                 oauth_token, 
#                 oauth_secret, 
#                 CONSUMER_KEY, 
#                 CONSUMER_SECRET))


#     tw.statuses.update(status=tweettext,
#                        in_reply_to_status_id=replyto)


def search_twitter(searchparameter):
    """ Twitter'daki son girilen tweetler içinde, verilen text'i arar. Bulunan son 100 tweet liste olarak ekrana ve dosyaya yazılır

    Parametreler:
        - searchparameter -- Aranılan keyword / text
    """
    activeCursor = -1
    searchThis = urllib.parse.quote(searchparameter.encode('utf-8'))
    searchThis = searchparameter

    tw = Twitter(auth=OAuth(
                oauth_token, 
                oauth_secret, 
                CONSUMER_KEY, 
                CONSUMER_SECRET))


    if IN_DEBUG_MODE:
        fn = open(SEARCH_RESULTS_FILE, "w+")

    print("Search String: {0}".format(searchThis) + "\n")

    print("{:25s} {:25s} {:25s}".format(
        "TwId", "Tweet", "Created"))
    print(
        "---------------------------------------------------------------------------------------------------------------------------------------------")

    if IN_DEBUG_MODE:
        fn.write("{0}\t{1}\t{2}\t".format("TweetId",
                                          "Tweet text",
                                          "Created At") + "\n")

    while activeCursor != 0:
        f = tw.search.tweets(q=searchThis, count=100)

        _lastInteraction = ""
        
        for tw in f["statuses"]:
            try:
                if (tw["id"]):
                    # TW standart tarih formatı: Sat Aug 11 12:51:00 +0000 2018
                    _tempDate = tw["created_at"]
                    dtObj = datetime.strptime(_tempDate, '%a %b %d %H:%M:%S %z %Y')
                    _lastInteraction = "{0:2}.{1:2}.{2}".format(
                        str(dtObj.day), str(dtObj.month), str(dtObj.year))

            except KeyError:
                _lastInteraction = "Not found"

            print("{:25s} {:25s} {:25s}".format(
                tw["id_str"], tw["text"], _lastInteraction))
            if IN_DEBUG_MODE:
                fn.write("{0}\t{1}\t{2}".format(
                    tw["id"], tw["text"], _lastInteraction) + "\n")

        activeCursor = 0

    if IN_DEBUG_MODE:
        fn.close()


def main():
    parser = argparse.ArgumentParser(description="Search twitter for specific text")
    parser.add_argument("-s", "--search",
                        dest="SEARCH_STRING",
                        help="Search string to be used in application",
                        metavar="search text")

    # parser.add_argument("-r", "--replyto",
    #                     dest="REPLY_TO",
    #                     help="Tweet id of the tweet that will be replied",
    #                     metavar="replyto Id")

    # parser.add_argument("-t", "--text",
    #                     dest="REPLY_TEXT",
    #                     help="Tweet that will be sent",
    #                     metavar="tweet text")

    args = parser.parse_args()
    if args.SEARCH_STRING:
        search_twitter(args.SEARCH_STRING)
    # elif args.REPLY_TO:
    #     replyto_tweet(args.REPLY_TO, args.REPLY_TEXT)


if __name__ == "__main__":
    main()
