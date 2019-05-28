'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, belirli bir tweet'i RT edenleri takipten çıkarmak ya da bloklamak için yazılmış deneme / sandbox kodu.
myTwitter.cfg dosyası içine ilgili değerlerin eklenmesi gerekmektedir.

Konfigürasyon dosyası değerleri:
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olacan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olacan CONSUMER SECRET>

IN_DEBUG_MODE = True ise, 
    Bloklanan ya da takipten çıkarılan kullanıcıların bilgilerini data/ dizini altındaki dosyaya yazar

Eğer bu koddan etkilenmesini istemediğiniz kullanıcılar varsa, onların user_id'lerini, twStart.py içindeki WhiteListUsers()
    listesine eklemeniz gerekiyor.

Komut satırından çalıştırma:
    python blockRTs.py 
        -t <Tweet ID>       : RT'lenen tweet'in ID'si (tweet'i browser'da açıp adres satırındaki numarayı kullanabilirsiniz)
        -s <True / False>   : Eğer "-s True" olarak kullanırsanız, blok, mute ya da unfollow işlemi için onayınızı sormaz. Direkt yapar.

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
from colorama import Fore, Back, Style, init
import gettext 

_ = gettext.gettext

IN_DEBUG_MODE: bool = False
TODAY_FORMATTED = datetime.today().strftime('%Y%m%d')

def BUM(tw, user, action):
    """ Block, Unfollow or Mute function based on the parameters. If user is in the WhiteList, then returns without
    doing anything.\n
    tw:     Twitter object that will be used in API calls,\n
    user:   UserId to be processed,\n
    action: 'B' for blocking, 'U' to unfollow and 'M' for muting.
    """

    if (user in twStart.WHITE_LIST_USERS):
        return

    if(action == "B"):
        print(_("Blocked: {0}").format(user))
        # TODO: Uncomment the code below
        # tw.blocks.create(user_id=usrId, skip_status=1, include_entities=False)
        return
    elif (action == "M"):
        print(_("Muted: {0}").format(user))
        # TODO: Uncomment the code below
        # tw.users.mutes(user_id=usrId)
        return
    elif(action == "U"):
        print(_("Unfollowed: {0}").format(user))
        # TODO: Uncomment the code below
        # tw.friendships.destroy(user_id=usrId)
    return

def blockRetweeters(TweetId, IsSilent):
    activeCursor = -1

    fileName = twStart.DATA_FOLDER + "/RTBlocked_" + TODAY_FORMATTED + ".txt"
    if(IN_DEBUG_MODE):
        fn = open(fileName, "w+")

    print("{:25s}{:25s}".format("User Id", "User Name"))
    print("-" * 100)

    if(IN_DEBUG_MODE):
        fn.write("{0}{1}".format("User Id", "User Name") + "\n")

    tw = twStart.hitTwitter()

    while activeCursor != 0:

        f = tw.statuses.retweeters.ids(cursor=activeCursor, count=100, _id=TweetId, stringify_ids=True)

        userIds = ",".join(f["ids"])
        users = tw.users.lookup(user_id=userIds)
        
        i = 0

        for usrId in f["ids"]:
            color = Fore.RED if usrId in twStart.WHITE_LIST_USERS else Fore.GREEN
            print(Style.BRIGHT + color + "{:25s} {:25s}".format(usrId, users[i]["screen_name"]))
            if(IN_DEBUG_MODE):
                fn.write("{0}\t{1}".format(usrId, users[i]["screen_name"]) + "\n")
            i+=1
        activeCursor = f["next_cursor"]

    if(IN_DEBUG_MODE):
        fn.close()

    print("-"*96)
    print(_("What do you want to do with all these users (case sensitive)?"))
    remove = input(_("[B]lock / [U]nfollow / [M]ute / [E]xit: "))
    
    if (IsSilent==False):
        RUsure = input(_("Are you sure? [Y]es / [N]o: "))
    else:
        RUsure = "Y"

    if(RUsure=="Y"):
        for usrId in f["ids"]:
            BUM(tw, usrId, remove)
        print (_("All done! Happy tweeting :) "))
        return

    print(_("Nothing to do here!"))

def main():
    parser = argparse.ArgumentParser(description=_("Blocks, mutes or unfollows specific Tweet's all retweeters."))
    parser.add_argument("-t",
                        dest="TWEET_ID",
                        help=_("Tweet Id to be used to define target users. All users those retweeted this one will be removed"))
    parser.add_argument("-s",
                        dest="SILENT",
                        help=_("If used, there won't be a confirmation for removal action."),
                        default=False)

    args = parser.parse_args()
    if args.TWEET_ID:
        blockRetweeters(args.TWEET_ID, args.SILENT)
    else:
        print(_("Please use -t parameter to define TweetId"))

if __name__ == "__main__":
    init(autoreset=True)
    main()
