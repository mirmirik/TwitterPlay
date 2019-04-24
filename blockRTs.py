'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, belirli bir tweet'i RT edenleri takipten çıkarmak ya da bloklamak için yazılmış deneme / sandbox kodu.
myTwitter.cfg dosyası içine ilgili değerleri ekleyip, komut satırından "python twPlay.py" yazarak çalıştırılabilir.

Konfigürasyon dosyası değerleri:
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olacan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olacan CONSUMER SECRET>

IN_DEBUG_MODE = True ise, 
    Bloklanan ya da takipten çıkarılan kullanıcıların bilgilerini data/ dizini altındaki dosyaya yazar

Komut satırından çalıştırma:
    python blockRTs.py -t <Tweet ID> -s <True / False>

Twitter API'ye erişim sağlayan wrapper library:
    https://github.com/sixohsix/twitter

Twitter User Object detayları:
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

Bir tweet'i RT edenleri alan API:
    https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-retweeters-ids

Geliştiriciler için kullanıcı ve hesap bilgilerinin kullanımı :
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview
'''

import twStart
from datetime import datetime
import argparse

IN_DEBUG_MODE: bool = False
TODAY_FORMATTED = datetime.today().strftime('%Y%m%d')

def blockRetweeters(TweetId, IsSilent):
    activeCursor = -1

    fileName = "data/RTBlocked_" + TODAY_FORMATTED + ".txt"
    if(IN_DEBUG_MODE):
        fn = open(fileName, "w+")

    print("{:25s}{:25s}".format("User Id", "User Name"))
    print("------------------------------------------------------------------------------------------------")

    if(IN_DEBUG_MODE):
        fn.write("{0}{1}".format("User Id", "User Name") + "\n")

    tw = twStart.hitTwitter()

    while activeCursor != 0:

        f = tw.statuses.retweeters.ids(cursor=activeCursor, count=100, _id=TweetId, stringify_ids=True)

        userIds = ",".join(f["ids"])
        users = tw.users.lookup(user_id=userIds)
        
        i = 0

        for usrId in f["ids"]:
            print("{:25s} {:25s}".format(usrId, users[i]["screen_name"]))
            if(IN_DEBUG_MODE):
                fn.write("{0}\t{1}".format(usrId, users[i]["screen_name"]) + "\n")
            i+=1
        activeCursor = f["next_cursor"]
    if(IN_DEBUG_MODE):
        fn.close()
    print("------------------------------------------------------------------------------------------------")
    print("What do you want to do with all these users?")
    remove = input("[B]lock / [U]nfollow / [M]ute / [E]xit: ")
    
    if (IsSilent==False):
        RUsure = input("Are you sure? [Y]es / [N]o: ")
    else:
        RUsure = "Y"

    if(RUsure=="Y"):
        if (remove == "B"):
            for usrId in f["ids"]:
                print("Blocked: {0}".format(usrId))
                # TODO: Kulanıcı bloklama kodu buraya gelecek
                # Şu kod iş görüyor olmalı: tw.blocks.create(user_id=usrId, skip_status=1, include_entities=False)
            print("All blocked :)")
            return
        if (remove == "M"):
            for usrId in f["ids"]:
                print("Muted: {0}".format(usrId))
                # TODO: Kulanıcıyı sessize alma kodu buraya gelecek
                # Şu kod iş görüyor olmalı: tw.users.mutes(user_id=usrId)
            print("All muted :)")
            return
        if (remove == "U"):
            for usrId in f["ids"]:
                print("Muted: {0}".format(usrId))
                # TODO: Kulanıcı takipten çıkarma kodu buraya gelecek
                # Şu kod iş görüyor olmalı: tw.friendships.destroy(user_id=usrId)
            print("All unfollowed :)")
            return
    
    print("Nothing to do here!")

def main():
    parser = argparse.ArgumentParser(description="Blocks, mutes or unfollows specific Tweet's all retweeters.")
    parser.add_argument("-t",
                        dest="TWEET_ID",
                        help="Tweet Id to be used to define target users. All users those retweeted this one will be removed")
    parser.add_argument("-s",
                        dest="SILENT",
                        help="If used, there won't be a confirmation for removal action.",
                        default=False)

    args = parser.parse_args()
    if args.TWEET_ID:
        blockRetweeters(args.TWEET_ID, args.SILENT)
    else:
        print("Please use -t parameter to define TweetId")

if __name__ == "__main__":
    main()
