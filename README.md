# TwitterPlay

Twitter API'sine bağlanıp, takipçi ve takip edilenler listesini almak için yazılmış deneme / sandbox kodu.
myTwitter.cfg dosyası içine ilgili değerleri ekleyip, komut satırından `python twPlay.py` yazarak çalıştırılabilir.

Konfigürasyon dosyası değerleri:
    
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olan CONSUMER SECRET>

    [runtime]
    FOLLOWER_FILE = Takipçilerin bilgilerinin yazılacağı text dosya ismi. DATA dizini içinde yaratılır. Tab delimeted dosya oluşturur.
    FOLLOWING_FILE = Takip edilenlerin bilgilerinin yazılacağı text dosya ismi. DATA dizini içinde yaratılır. Tab delimeted dosya oluşturur.

IN_DEBUG_MODE = True ise,
    tüm ilgili kullanıcı nesnesine ait bilgiler "raw_data.json" isimli dosyaya da JSON formatında yazılır. Buradaki alanlar incelenip ihtiyca göre kullanıcılara ait farklı bilgilere de erişim sağlanabilir.

Twitter API'ye erişim sağlayan wrapper library:

https://github.com/sixohsix/twitter

Twitter User Object detayları:

https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

Geliştiriciler için kullanıcı ve hesap bilgilerinin kullanımı :

https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview

Author: Tolga MIRMIRIK (@mirmirik)
