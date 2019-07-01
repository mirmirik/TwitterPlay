'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, parametre olarak verilen kullanıcıyı takip edenleri takipten çıkarmak için yazılmış deneme / sandbox kodu.

myTwitter.cfg dosyası içine ilgili değerlerin eklenmesi gerekmektedir.

Konfigürasyon dosyası değerleri:
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olacan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olacan CONSUMER SECRET>

IN_DEBUG_MODE = True ise, 
    Takipten çıkarılan kullanıcıların bilgilerini data/ dizini altındaki dosyaya yazar

Eğer bu koddan etkilenmesini istemediğiniz kullanıcılar varsa, onların user_id'lerini, twStart.py içindeki WhiteListUsers()
    listesine eklemeniz gerekiyor.

Komut satırından çalıştırma:
    python unFollowUsersFriends.py 
        -u <user_name>      : Hangi kullanıcının takipçileri çıkarılmak isteniliyorsa onun kullanıcı adı.
        -s <True / False>   : Eğer "-s True" olarak kullanırsanız, blok, mute ya da unfollow işlemi için onayınızı sormaz. Direkt yapar.

Twitter API'ye erişim sağlayan wrapper library:
    https://github.com/sixohsix/twitter

Twitter User Object detayları:
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

Bir kullanıcıyı takip edenleri veren method:
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-friends-ids

Geliştiriciler için kullanıcı ve hesap bilgilerinin kullanımı :
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview
'''

import twStart
from datetime import datetime
import argparse
from colorama import Fore, Back, Style, init
import pprint

IN_DEBUG_MODE: bool = True
TODAY_FORMATTED = datetime.today().strftime('%Y%m%d')

def unfollowUsersFriends(UserName, IsSilent):
    activeCursor = -1

    fileName = twStart.DATA_FOLDER + "/unFollowUsersFriends_" + TODAY_FORMATTED + ".txt"
    if(IN_DEBUG_MODE):
        fn = open(fileName, "w+")

    tw = twStart.hitTwitter()

    nemesisFriends = []
    myFriends = []

    while activeCursor != 0:
        f = tw.followers.ids(cursor=activeCursor, count=2048, stringify_ids=True, screen_name=UserName)
        nemesisFriends += f["ids"]
        activeCursor = f["next_cursor"]
    
    print("Nemesis's friends count: {}".format(len(nemesisFriends)))

    activeCursor = -1
    while activeCursor != 0:
        f = tw.friends.ids(cursor=activeCursor, count=2048, stringify_ids=True)
        myFriends += f["ids"]
        activeCursor = f["next_cursor"]

    print("My friends count: {}".format(len(myFriends)))

    commonFriendsList = list(set(nemesisFriends) & set(myFriends))
    print("Common friends count: {}".format(len(commonFriendsList)))

    print(Style.BRIGHT + Fore.GREEN + "{:25s}{:25s}".format("User Id", "User Name"))
    print(Style.BRIGHT + Fore.GREEN + "-" * 70)

    if(IN_DEBUG_MODE):
        fn.write("{0}{1}\n".format("User Id", "User Name"))

    userIds = ",".join(commonFriendsList)
    users = tw.users.lookup(user_id=userIds)

    for user in users:
        if user["id_str"] in twStart.WHITE_LIST_USERS:
            # twStart.sendMessage(tw, user["id_str"], "WUT?")
            color = Fore.RED  
        else:
            Fore.GREEN
        print(color + "{:25s} {:25s}".format(user["id_str"], user["screen_name"]))
        if(IN_DEBUG_MODE):
            fn.write("{0}\t{1}".format(user["id_str"], user["screen_name"]) + "\n")

    if(IN_DEBUG_MODE):
        fn.close()

    print(Style.BRIGHT + Fore.GREEN + "-"*96)
    
    if (IsSilent==False):
        RUsure = input(Style.BRIGHT + Fore.RED + "Are you sure? [Y]es / [N]o: ")
        print(Style.BRIGHT + Fore.GREEN + "-"*96)
    else:
        RUsure = "Y"

    if(RUsure=="Y"):
        for user in users:
            twStart.BUM(tw, user["screen_name"], user["id_str"], "U")
        print ("All done! Happy tweeting :) ")
        return

    print("Nothing to do here!")

def main():
    parser = argparse.ArgumentParser(description="Unfollows common friends with the given user name.")
    parser.add_argument("-u",
                        dest="USERNAME",
                        help="User's twitter account name.")

    parser.add_argument("-s",
                        dest="SILENT",
                        help="If true, no confirmation dialog will be displayed for removal action.",
                        default=False)

    args = parser.parse_args()
    if args.USERNAME:
        unfollowUsersFriends(args.USERNAME, args.SILENT)
    else:
        print("Please use -u parameter to define user name...")

if __name__ == "__main__":
    init(autoreset=True)
    main()
