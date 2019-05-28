'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, takip edilen kullanıcılardan rastgele %50'sini takipten çıkarmak, 
sessize almak ya da bloklamak için yazılmış deneme / sandbox kodu.

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
    python twThanos.py 
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
import random
import pprint

IN_DEBUG_MODE: bool = True
TODAY_FORMATTED = datetime.today().strftime('%Y%m%d')

def listUnluckyFriends(tw, selectedOnes, sliceStart, sliceEnd, unluckyGuysCount, usersToBeDestroyed):
    newArray = selectedOnes[sliceStart:sliceEnd]
    userIds = ""
    userIds = ",".join(map(str, newArray))
    users = tw.users.lookup(user_id=userIds)
    for user in users:
        unluckyGuysCount += 1
        usersToBeDestroyed[unluckyGuysCount] = {}
        randomAction = str(random.choice(['B', 'U', 'M']))
        usersToBeDestroyed[unluckyGuysCount]["user_id"] = user["id_str"]
        usersToBeDestroyed[unluckyGuysCount]["user_name"] = user["screen_name"]
        usersToBeDestroyed[unluckyGuysCount]["action"] = randomAction
    
    return usersToBeDestroyed, unluckyGuysCount


def destroyHalfPercent(IsSilent):
    activeCursor = -1
    maxArraySize = 100
    usersToBeDestroyed = {1:{}}
    unluckyGuysCount = 0

    fileName = twStart.DATA_FOLDER + "/twThanosDestroyed_" + TODAY_FORMATTED + ".txt"
    if(IN_DEBUG_MODE):
        fn = open(fileName, "w+")

    print("{:25s}{:25s}{:25s}".format("User Id", "User Name", "Action"))
    print("-" * 100)

    if(IN_DEBUG_MODE):
        fn.write("{0}{1}{2}\n".format("User Id", "User Name", "Action"))

    tw = twStart.hitTwitter()

    allUserIds = []

    while activeCursor != 0:
        f = tw.friends.ids(cursor=activeCursor, count=2048, stringify_ids=True)
        allUserIds += f["ids"]
        activeCursor = f["next_cursor"]

    halfOfTheUsers = len(allUserIds) // 2
    
    sRandom = random.SystemRandom()
    selectedUsers = sRandom.choices(allUserIds, k=halfOfTheUsers)

    modulus, fixed = twStart.splitArray(halfOfTheUsers, maxArraySize)

    for x in range(fixed):
        usersToBeDestroyed, unluckyGuysCount = listUnluckyFriends(tw, selectedUsers, (x*maxArraySize), (x*maxArraySize+maxArraySize), unluckyGuysCount, usersToBeDestroyed)
    usersToBeDestroyed, unluckyGuysCount = listUnluckyFriends(tw, selectedUsers, (halfOfTheUsers-modulus), (halfOfTheUsers+modulus), unluckyGuysCount, usersToBeDestroyed)

    for i in range(1, unluckyGuysCount):
        color = Fore.RED if usersToBeDestroyed[i]["user_id"] in twStart.WHITE_LIST_USERS else Fore.GREEN
        print(Style.BRIGHT + color + "{:25s} {:25s} {:25s}".format(usersToBeDestroyed[i]["user_id"], usersToBeDestroyed[i]["user_name"], usersToBeDestroyed[i]["action"]))
        if(IN_DEBUG_MODE):
            fn.write("{0}\t{1}\t{2}".format(usersToBeDestroyed[i]["user_id"], usersToBeDestroyed[i]["user_name"], usersToBeDestroyed[i]["action"]) + "\n")

    if(IN_DEBUG_MODE):
        fn.close()

    print("-"*96)
    
    if (IsSilent==False):
        RUsure = input("Are you sure? [Y]es / [N]o: ")
    else:
        RUsure = "Y"

    if(RUsure=="Y"):
        for i in range(1, unluckyGuysCount):
            twStart.BUM(tw, usersToBeDestroyed[i]["user_name"], usersToBeDestroyed[i]["user_id"], usersToBeDestroyed[i]["action"])
        print ("All done! Happy tweeting :) ")
        return

    print("Nothing to do here!")

def main():
    parser = argparse.ArgumentParser(description="Blocks, mutes or unfollows randomly selected friends.")
    parser.add_argument("-s",
                        dest="SILENT",
                        help="If true, no confirmation dialog will be displayed for removal action.",
                        default=False)

    args = parser.parse_args()
    destroyHalfPercent(args.SILENT)

if __name__ == "__main__":
    init(autoreset=True)
    main()
