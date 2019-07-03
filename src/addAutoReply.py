'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, parametre olarak verilen kelime/kelime grubunu aktif kullanıcının timeline'ında arar.
Her bulduğu tweet altına, "mesaj" parametresi ile verilen text!i ekler. Deneme / sandbox kodudur.

myTwitter.cfg dosyası içine ilgili değerlerin eklenmesi gerekmektedir.

Konfigürasyon dosyası değerleri:
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olacan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olacan CONSUMER SECRET>

IN_DEBUG_MODE = True ise, 
    Takipten çıkarılan kullanıcıların bilgilerini data/ dizini altındaki dosyaya yazar

Komut satırından çalıştırma:
    python addAutoReply.py -s <aranacak kelime> -m <reply olarak eklnecek yazı>  

Bir cron job ile belli süreler ile tekrarlı çalıştırılarak kullanılabilir. 

Twitter API'ye erişim sağlayan wrapper library:
    https://github.com/sixohsix/twitter

Twitter Home Timeline:
    https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-home_timeline.html

Geliştiriciler için kullanıcı ve hesap bilgilerinin kullanımı :
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview
'''

import twStart
from datetime import datetime
import argparse
import json

IN_DEBUG_MODE: bool = True
TODAY_FORMATTED = datetime.today().strftime('%Y%m%d')

def SearchTimeline(tw, searchText):
    timeline = tw.statuses.home_timeline(count=200)
    foundedIndex = 0
    foundTweets = {1:{}}

    for timeline_tweet in timeline:
        if (str(timeline_tweet["text"]).find(searchText)) > -1:
            foundedIndex += 1
            foundTweets[foundedIndex] = {}
            foundTweets[foundedIndex]["tweet_id"] = timeline_tweet["id_str"]
            foundTweets[foundedIndex]["user_id"] = timeline_tweet["user"]["id_str"]
            foundTweets[foundedIndex]["user_name"] = timeline_tweet["user"]["name"]

    return foundTweets, foundedIndex

def AddReplyToTweet(tw, tweetId, message):
    # TODO: Uncomment the code below to be able to add a reply
    # tw.statuses.update(status=message,
    #                  in_reply_to_status_id=tweetId)
    pass

def AutoReplyToTweets(searchText, message):
    tw = twStart.hitTwitter()

    targetedTweets, totalTweetCount = SearchTimeline(tw, searchText)

    # jsDump = json.dumps(targetedTweets, indent=4, sort_keys=True)
    # print(jsDump)

    fileName = twStart.DATA_FOLDER + "/AutoRepliedTweets_" + TODAY_FORMATTED + ".txt"
    fn = open(fileName, "a+")
    fn = open(fileName, "r")
    repliedTweets = fn.read()
    fn = open(fileName, "a+")

    for i in range(1, totalTweetCount):
        if (targetedTweets[i]["tweet_id"] not in repliedTweets):
            fn.write(targetedTweets[i]["tweet_id"] + "\n")
            print("User replied: {0}".format(targetedTweets[i]["user_name"]))
            # TODO: Uncomment the code below to be able to add a reply
            # AddReplyToTweet(tw, targetedTweets[i]["tweet_id"], message):
    print ("All done! Happy tweeting :)\n")

    fn.close()

    return

def main():
    parser = argparse.ArgumentParser(description="Adds an auto-reply message to specific tweets in timeline.")
    parser.add_argument("-s",
                        dest="SEARCH_TEXT",
                        help="Text to be searched in timeline.",
                        default="İskender")

    parser.add_argument("-m",
                        dest="MESSAGE",
                        help="Message to be added as a reply to tweet.",
                        default="Auto-reply")

    args = parser.parse_args()
    if args.SEARCH_TEXT:
        AutoReplyToTweets(args.SEARCH_TEXT, args.MESSAGE)
    else:
        print("Please use -s parameter to search in timeline of active user...")

if __name__ == "__main__":
    main()
