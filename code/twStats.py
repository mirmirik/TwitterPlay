'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, authenticate olmuş kullanıcının istatistiklerini çıkarmak için yazılmış deneme / sandbox kodu.
myTwitter.cfg dosyası içine ilgili değerleri ekleyip, komut satırından "python twMyStats.py" yazarak çalıştırılabilir. 1500'den
fazla takipçisi olan kullanıcılar için ne yazık ki Twitter Standard API kısıtlamasına takılıyor (15min --> 15req / 100 users per request) :(

Konfigürasyon dosyası değerleri:
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olacan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olacan CONSUMER SECRET>

Twitter API'ye erişim sağlayan wrapper library:
    https://github.com/sixohsix/twitter

Twitter User Object detayları:
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

pyMyStats kodunda kullanılan API Reference (friendship-lookup, folllowers-ids, friends-ids):
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-friends-ids
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-followers-ids
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-friendships-lookup

    JSON from 'lookup' return:
            {
                "name": "Harrison Test",
                "screen_name": "Harris_0ff",
                "id": 4337869213,
                "id_str": "4337869213",
                "connections": [
                    "following",
                    "following_requested",
                    "followed_by"
                    ]
            }
    "connections" değerleri: "following, following_requested, followed_by, none, blocking, muting"

Geliştiriciler için kullanıcı ve hesap bilgilerinin kullanımı :
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview
'''

import twStart
from datetime import datetime

TODAY_FORMATTED = datetime.today().strftime('%Y%m%d')

activeCursor = -1

myStats = {
    "followers": 0,
    "following": 0,
    "muted_me": 0,
    "i_ve_muted": 0,
    "i_follow_but_they_dont": 0,
    "they_follow_but_i_dont": 0,
    "we_both_follow_each_other": 0,
    "mysterious_followers_that_i_dont_follow": 0
}

print("{:25s} {:25s} {:25s} {:25s} {:25s} {:25s}".format(
    "Name", "Muted", "IFollow", "TheyFollow", "Both", "Hidden"))
print("---------------------------------------------------------------------------------------------------------------------------------------------")

ntw = twStart.hitTwitter()
follower_ids = ntw.followers.ids(screen_name="mirmirik")
all_ids = follower_ids["ids"]

print (all_ids[:100])


