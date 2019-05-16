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
import pprint
import json
from dateutil import relativedelta


TODAY_FORMATTED = datetime.today().strftime('%Y%m%d')

rules = { 'LAST_STATUS_UPDATE_IN_MONTHS': 1, 
            'ACCOUNT_CREATED_YEAR': date.today().year,
            'ACCOUNT_CREATED_MONTH': date.today().month }

def removeFriend():
    activeCursor = -1

    tw = twStart.hitTwitter()

    removeFriendCount = 0
    removeableUsers = {1:{}}

    while activeCursor != 0:

        f = tw.friends.list(cursor=activeCursor, count=200)

        lastInteraction = ""

        for usr in f["users"]:
            try: 
                if (usr["status"]):
                    lastInteraction = twStart.FormatTwitterDate(usr["status"]["created_at"], 'D')
                    accountCreated = twStart.FormatTwitterDate(usr["created_at"], 'D')

                    r = relativedelta.relativedelta(datetime.today(), lastInteraction)

                    accountCreation_Rule = (accountCreated.year == rules['ACCOUNT_CREATED_YEAR'] 
                            and accountCreated.month == rules['ACCOUNT_CREATED_MONTH'])
                    
                    lastInteraction_Rule = (r.months > rules['LAST_STATUS_UPDATE_IN_MONTHS'])

                    userIsNotInWhitelist = usr["id_str"] not in twStart.WHITE_LIST_USERS

                    if (
                        (accountCreation_Rule or lastInteraction_Rule) and userIsNotInWhitelist
                        ):
                        removeFriendCount += 1
                        lastInteractionJSON = twStart.FormatTwitterDate(usr["status"]["created_at"], 'S')
                        accountCreatedJSON = twStart.FormatTwitterDate(usr["created_at"], 'S')
                        removeableUsers[removeFriendCount] = {}
                        removeableUsers[removeFriendCount]["user_id"] = usr["id_str"]
                        removeableUsers[removeFriendCount]["user_name"] = usr["name"]
                        removeableUsers[removeFriendCount]["account_created"] = accountCreatedJSON
                        removeableUsers[removeFriendCount]["last_interaction"] = lastInteractionJSON
                        if(lastInteraction_Rule):
                            removeableUsers[removeFriendCount]["remove_reason"] = "Last interaction date is too old."
                        elif accountCreation_Rule:
                            removeableUsers[removeFriendCount]["remove_reason"] = "Account is too young."
                        
            except: # status alınamıyorsa, kullanıcı "kilitli" hesaba sahiptir.
                lastInteraction = "Not found"

        activeCursor = f["next_cursor"]

    ''' Test commands '''
    # pprint.pprint(removeableUsers)
    # jsDump = json.dumps(removeableUsers, indent=4, sort_keys=True)
    # print(jsDump)

    print("{:10s} {:25s} {:35s}".format("Index", "User Name", "Reason"))
    print("-" * 90)

    for i in range(1, removeFriendCount):
        print("{:10d} {:25s} {:35s}".format(i, removeableUsers[i]["user_name"], removeableUsers[i]["remove_reason"]))

    print("="*96 + "\n\n")

    print("These users will be UNFOLLOWED. Are you sure? (case sensitive)?")
    RUsure = input("Are you sure? [Y]es / [N]o: ")

    if(RUsure=="Y"):
        for i in range(1, removeFriendCount):
            print("Unfollowed: {0}".format(removeableUsers[i]["user_name"]))
            # TODO: Kulanıcı takipten çıkarma kodu açılmalı
            # İşler hale gelmesi için aşağıdaki satırı açmalısınız
            # tw.friendships.destroy(user_id=removeableUsers[i]["user_id"])
        print ("All done! Happy tweeting :) ")
        return

    print("Nothing to do here!")

if __name__ == "__main__": 
    removeFriend()