[![Board Status](https://dev.azure.com/testeryou/10b2e0c2-0062-4680-b034-4362f128ab46/0eb5b43d-0494-46b9-a50e-cb7d9a661067/_apis/work/boardbadge/46c90235-e619-492e-97b0-2ba372d4fce9?columnOptions=1)](https://dev.azure.com/testeryou/10b2e0c2-0062-4680-b034-4362f128ab46/_boards/board/t/0eb5b43d-0494-46b9-a50e-cb7d9a661067/Microsoft.RequirementCategory)

# TwitterPlay

Twitter API'sine bağlanıp, takipçi ve takip edilenler listesini almak için yazılmış deneme / sandbox kodu.
myTwitter.cfg dosyası içine ilgili değerleri ekleyip, komut satırından `python <ilgili dosya>` yazarak çalıştırılabilir.
Text dosya çıktıları, kodun çalıştığı dizin altındaki "DATA" dizini içine, günün tarihi ile eklenir.

Konfigürasyon dosyası değerleri:
    
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olan CONSUMER SECRET>

IN_DEBUG_MODE = True ise,
    tüm ilgili kullanıcı nesnesine ait bilgiler twPlay.py çalıştırıldığında "raw_data.json" isimli dosyaya da JSON formatında yazılır. Buradaki alanlar incelenip ihtiyca göre kullanıcılara ait farklı bilgilere de erişim sağlanabilir.

Çıktı dosyaları:

    followers_YYYYMMDD.txt  -> Takip edenler    (twPlay.py)
    following_YYYYMMDD.txt  -> Takip edilenler  (twPlay.py)
    RTBlocked_YYYYMMDD.txt  -> Bloklanmaya aday olanlar  (blockRTs.py)

    Sonraki sürümlerde planlanan
    myStats_YYYYMMDD.txt    -> İstatistikler    (twMyStats.py) 

Python öğrenim için kaynak:

http://www.veridefteri.com

Twitter API'ye erişim sağlayan wrapper library:

https://github.com/sixohsix/twitter

Twitter User Object detayları:

https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

Geliştiriciler için kullanıcı ve hesap bilgilerinin kullanımı :

https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview

pyMyStats kodunda kullanılan API Reference (friendship-lookup, folllowers-ids, friends-ids):

    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-friends-ids
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-followers-ids
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-friendships-lookup


Author: Tolga MIRMIRIK (@mirmirik)
