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
    myStats_YYYYMMDD.txt    -> İstatistikler    (twMyStats.py)

Python öğrenim için kaynak:

http://www.veridefteri.com

Twitter API'ye erişim sağlayan wrapper library:

https://github.com/sixohsix/twitter

Twitter User Object detayları:

https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

Geliştiriciler için kullanıcı ve hesap bilgilerinin kullanımı :

https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview

pyMyStats kodunda kullanılan API Reference (friendship-lookup):

https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-friendships-lookup

Author: Tolga MIRMIRIK (@mirmirik)
