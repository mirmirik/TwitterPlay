'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, blokladığınız ve MUTE yaptığınız kullanıcıları listeleyen ve bunları 
geri almaya yarayan(UnBlock / UnMute) deneme / sandbox kodu.

myTwitter.cfg dosyası içine ilgili değerlerin eklenmesi gerekmektedir.

Konfigürasyon dosyası değerleri:
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olacan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olacan CONSUMER SECRET>

IN_DEBUG_MODE = True ise, 
    Bloklanan ya da sessize alınan kullanıcıların bilgilerini data/ dizini altındaki dosyaya yazar

Eğer bu koddan etkilenmesini istemediğiniz kullanıcılar varsa, onların user_id'lerini, twStart.py içindeki WhiteListUsers()
    listesine eklemeniz gerekiyor.

Komut satırından çalıştırma:
    python undoThanos.py 
        -t <B / M>          : 'B' --> Blocked listesi üzerinden işlem yapar, 'M' --> Muted kullanıcılar listesi üzerinden
        -s <True / False>   : Eğer "-s True" olarak kullanırsanız, unblok ya da unmute işlemi için onayınızı sormaz. Direkt yapar.

Twitter API'ye erişim sağlayan wrapper library:
    https://github.com/sixohsix/twitter

Twitter User Object detayları:
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

Sessize alınan kullanıcılar ile ilgili API metodları:
    https://developer.twitter.com/en/docs/accounts-and-users/mute-block-report-users/api-reference/get-mutes-users-list
    https://developer.twitter.com/en/docs/accounts-and-users/mute-block-report-users/api-reference/post-mutes-users-destroy

Blok ile ilgili API metodları:
    https://developer.twitter.com/en/docs/accounts-and-users/mute-block-report-users/api-reference/get-blocks-list
    https://developer.twitter.com/en/docs/accounts-and-users/mute-block-report-users/api-reference/post-blocks-destroy

Geliştiriciler için kullanıcı ve hesap bilgilerinin kullanımı :
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview
'''

import twStart
from datetime import datetime
import argparse
from colorama import Fore, Back, Style, init

IN_DEBUG_MODE: bool = False
TODAY_FORMATTED = datetime.today().strftime('%Y%m%d')

def undoBlockMute(tw, user, action):
    """ Bloklanan ya da sessize alınan kulanıcıları açmaya yarayan metod.\n
    tw:     API çağrıları için kullanılan twitter nesnesi,\n
    user:   Kullanıcı ID,\n
    action: 'B' --> UnBlock, 'M' --> UnMute
    """

    if (user in twStart.BLACK_LIST_USERS):
        return

    if(action == "B"):
        print("Blok kaldırıldı: {0}".format(user))
        # TODO: Kulanıcı unbloklama kodu açılmalı
        # İşler hale gelmesi için aşağıdaki satırı açmalısınız
        # tw.blocks.destroy(user_id=usrId, skip_status=1, include_entities=False)
        return
    elif (action == "M"):
        print("Mute kaldırıldı: {0}".format(user))
        # TODO: Kulanıcıyı sessize alma kodu açılmalı
        # İşler hale gelmesi için aşağıdaki satırı açmalısınız
        # tw.mutes.users.destroy(user_id=usrId)
        return
    return

def listUsers(userAction, IsSilent):
    activeCursor = -1

    fileName = twStart.DATA_FOLDER + "/undoThanos_" + userAction + "_" + TODAY_FORMATTED + ".txt"
    if(IN_DEBUG_MODE):
        fn = open(fileName, "w+")

    print("{:25s}{:25s}".format("User Id", "User Name"))
    print("-" * 100)

    if(IN_DEBUG_MODE):
        fn.write("{0}{1}".format("User Id", "User Name") + "\n")

    tw = twStart.hitTwitter()

    while activeCursor != 0:
        if (userAction == 'B'):
            f = tw.blocks.ids(cursor=activeCursor, stringify_ids=True)
        elif (userAction == 'M'):
            f = tw.mutes.users.ids(cursor=activeCursor, stringify_ids=True)

        userIds = ",".join(f["ids"])
        users = tw.users.lookup(user_id=userIds)
        
        i = 0

        for usrId in f["ids"]:
            color = Fore.GREEN if usrId in twStart.BLACK_LIST_USERS else Fore.RED
            print(Style.BRIGHT + color + "{:25s} {:25s}".format(usrId, users[i]["screen_name"]))
            if(IN_DEBUG_MODE):
                fn.write("{0}\t{1}".format(usrId, users[i]["screen_name"]) + "\n")
            i+=1
        activeCursor = f["next_cursor"]

    if(IN_DEBUG_MODE):
        fn.close()

    print("-"*96)

    if (IsSilent==False):
        RUsure = input("These users will be un" + ("blocked" if userAction=='B' else "muted") + ". Are you sure? [Y]es / [N]o: ")
    else:
        RUsure = "Y"

    if(RUsure=="Y"):
        for usrId in f["ids"]:
            undoBlockMute(tw, usrId, userAction)
        print ("All done! Happy tweeting :) ")
        return

    print("Nothing to do here!")

def main():
    parser = argparse.ArgumentParser(description="Blocks, mutes or unfollows specific Tweet's all retweeters.")
    parser.add_argument("-t",
                        dest="ACTION",
                        help="B: Unblock, M: Unmute")
    parser.add_argument("-s",
                        dest="SILENT",
                        help="If used, there won't be a confirmation for removal action.",
                        default=False)

    args = parser.parse_args()
    if args.ACTION:
        listUsers(args.ACTION, args.SILENT)
    else:
        print("Please use -t parameter to define action")

if __name__ == "__main__":
    init(autoreset=True)
    main()
