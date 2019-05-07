'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, takipçi ve takip edilenler listesini almak için yazılmış deneme / sandbox kodu.
myTwitter.cfg dosyası içine ilgili değerleri ekleyip, komut satırından "python twPlay.py" yazarak çalıştırılabilir.

Konfigürasyon dosyası değerleri:
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olacan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olacan CONSUMER SECRET>

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

import twStart
from datetime import datetime
import json, os

IN_DEBUG_MODE: bool = False
GET_FOLLOWERS: bool = False

TODAY_FORMATTED = datetime.today().strftime('%Y%m%d')

def getTwitterData():
    activeCursor = -1

    fileName = "/follower_" + TODAY_FORMATTED + ".txt" if GET_FOLLOWERS else "/following_" + TODAY_FORMATTED + ".txt"

    fn = open(twStart.DATA_FOLDER + fileName, "w+")

    print("{:10s} {:25s} {:25s} {:25s} {:25s} {:25s} {:25s} {:25s}".format(
        "Index", "Screen Name", "Name", "ID", "Follower-Friend", "Last Interaction", "Account Created", "Protected"))
    print("-" * 190)

    fn.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}".format("screen_name",
                                                    "name",
                                                    "id_str",
                                                    "followers_count", 
                                                    "friends_count",
                                                    "flwr_frnds",
                                                    "last_interaction",
                                                    "acc_created",
                                                    "protected") + "\n")

    tw = twStart.hitTwitter()

    index = 1

    while activeCursor != 0:

        f = tw.followers.list(cursor=activeCursor, count=500) if GET_FOLLOWERS else tw.friends.list(cursor=activeCursor, count=200)

        _lastInteraction = ""
        for usr in f["users"]:
            try:
                if (usr["status"]):
                    # status alınamıyorsa, kullanıcı "kilitli" hesaba sahiptir.
                    # TW standart tarih formatı: Sat Aug 11 12:51:00 +0000 2018
                    _tempDate = usr["status"]["created_at"]
                    lastStatusDate = datetime.strptime(_tempDate, '%a %b %d %H:%M:%S %z %Y')
                    _lastInteraction = "{2}{1}{0}".format(
                        str(lastStatusDate.day).zfill(2), 
                        str(lastStatusDate.month).zfill(2), 
                        str(lastStatusDate.year))

                    # En son 2019'dan önce tweet atmışları takipten çıkaralım.
                    if (lastStatusDate.year < 2019):
                        tw.friendships.destroy(user_id=usr["id_str"])
                    
                    dtObj = datetime.strptime(usr["created_at"], '%a %b %d %H:%M:%S %z %Y')
                    _accountCreated = "{2}{1}{0}".format(
                        str(dtObj.day).zfill(2), 
                        str(dtObj.month).zfill(2), 
                        str(dtObj.year))

            except:
                _lastInteraction = "Not found"

            try:
                _follower_friend_ratio = usr["followers_count"] / usr["friends_count"] 
            except:
                _follower_friend_ratio = usr["followers_count"]

            print("{:4d} {:25s} {:25s} {:25s} {:6.4f} {:25s} {:25s} {:25s}".format(
                index,
                usr["screen_name"], 
                usr["name"], 
                usr["id_str"], 
                _follower_friend_ratio, 
                _lastInteraction, 
                _accountCreated, 
                str(usr["protected"])))


            fn.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}".format(
                usr["screen_name"], 
                usr["name"], 
                usr["id_str"], 
                usr["followers_count"], 
                usr["friends_count"], 
                _follower_friend_ratio,
                _lastInteraction, 
                _accountCreated,
                str(usr["protected"]) + "\n"))

            index += 1

        activeCursor = f["next_cursor"]
        if IN_DEBUG_MODE:
            with open(twStart.DATA_FOLDER + "/raw_data.json", "w+") as fl:
                jsDump = json.dumps(f, indent=4, sort_keys=False)
                fl.write(jsDump)
    fn.close()

if __name__ == "__main__": 
    getTwitterData()