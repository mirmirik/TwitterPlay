'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, takip edilenleri belirli kurallar çerçevesinde takipten çıkarmak için yazılmış deneme / sandbox kodu.
myTwitter.cfg dosyası içine ilgili değerleri ekleyip, komut satırından "python twPlay.py" yazarak çalıştırılabilir.

Konfigürasyon dosyası değerleri:
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olacan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olacan CONSUMER SECRET>

Twitter API'ye erişim sağlayan wrapper library:
    https://github.com/sixohsix/twitter

Twitter User Object detayları:
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

Geliştiriciler için kullanıcı ve hesap bilgilerinin kullanımı :
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview
'''

import twStart
from datetime import datetime, date

TODAY_FORMATTED = datetime.today().strftime('%Y%m%d')

rules = { 'LAST_STATUS_UPDATE': 6, 
            'ACCOUNT_CREATED_YEAR': 2008, #date.today().year,
            'ACCOUNT_CREATED_MONTH': date.today().month }

def removeFriend():
    activeCursor = -1

    tw = twStart.hitTwitter()

    removeFriendCount = 1

    while activeCursor != 0:

        f = tw.friends.list(cursor=activeCursor, count=200)

        lastInteraction = ""
        removeableUsers = {0:{}}

        for usr in f["users"]:
            try: 
                if (usr["status"]):
                    lastInteraction = twStart.FormatTwitterDate(usr["status"]["created_at"], 'D')
                    accountCreated = twStart.FormatTwitterDate(usr["created_at"], 'D')
                    # En son 2019'dan önce tweet atmışları takipten çıkaralım.
                    if (accountCreated.year < rules['ACCOUNT_CREATED_YEAR']):
                        lastInteraction = twStart.FormatTwitterDate(usr["status"]["created_at"], 'S')
                        accountCreated = twStart.FormatTwitterDate(usr["created_at"], 'S')
                        removeableUsers = {removeFriendCount: {}}
                        removeableUsers[removeFriendCount]["user_id"] = usr["id_str"]
                        removeableUsers[removeFriendCount]["user_name"] = usr["name"]
                        removeableUsers[removeFriendCount]["account_created"] = accountCreated
                        removeableUsers[removeFriendCount]["last_interaction"] = lastInteraction
                        removeableUsers[removeFriendCount]["remove_reason"] = "Last interaction date is too old."
                        removeFriendCount += 1
                    #     tw.friendships.destroy(user_id=usr["id_str"])
            except: # status alınamıyorsa, kullanıcı "kilitli" hesaba sahiptir.
                lastInteraction = "Not found"

            # print("{:4d} {:25s} {:25s} {:25s} {:25s}".format(
            #     removeFriendCount,
            #     usr["screen_name"], 
            #     usr["name"], 
            #     lastInteraction, 
            #     accountCreated
            #     ))

        activeCursor = f["next_cursor"]


    print(removeableUsers)
    
    for p_id, p_info in removeableUsers.items():
        print("\nremoveFriendCount:", p_id)
        for key in p_info:
            print(key + ':', p_info[key])



if __name__ == "__main__": 
    # t = "Sat Aug 19 12:51:00 +0000 2019"
    # print (twStart.FormatTwitterDate(t, 'S'))
    # print(twStart.FormatTwitterDate(t,'D'))
    # print(twStart.FormatTwitterDate(t))
    removeFriend()