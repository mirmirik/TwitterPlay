[![Board Status](https://dev.azure.com/testeryou/10b2e0c2-0062-4680-b034-4362f128ab46/0eb5b43d-0494-46b9-a50e-cb7d9a661067/_apis/work/boardbadge/46c90235-e619-492e-97b0-2ba372d4fce9?columnOptions=1)](https://dev.azure.com/testeryou/10b2e0c2-0062-4680-b034-4362f128ab46/_boards/board/t/0eb5b43d-0494-46b9-a50e-cb7d9a661067/Microsoft.RequirementCategory) ![GitHub](https://img.shields.io/github/license/mirmirik/TwitterPlay.svg)
![GitHub top language](https://img.shields.io/github/languages/top/mirmirik/TwitterPlay.svg) ![GitHub last commit](https://img.shields.io/github/last-commit/mirmirik/TwitterPlay.svg)
# TwitterPlay

Twitter API'sine bağlanıp, metodları test etmek için yazılmış deneme / sandbox kodları.
myTwitter.cfg dosyası içine ilgili değerleri ekleyip, komut satırından `python <ilgili dosya> [parametreler]` yazarak çalıştırılabilir.
Eğer kod içinde bir çıktı varsa, proje dizini altındaki "DATA" dizini içine, günün tarihi ile eklenir.

## Konfigürasyon dosyası değerleri:
    
`./config/twitter.cfg` dosyasını, `./config/myTwitter.cfg` olarak değiştirip kullanabilirsiniz. Dosya içine yazılacak değerler aşağıdaki gibidir:

```python
[auth]
ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olan CONSUMER KEY>
CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olan CONSUMER SECRET>
```
## Yapılan geliştirmeler:

Yazılan kodların tamamı `./src/`dizini altındadır. `./tests/` dizini altında pyTest kullanan test kodları eklenecektir. `./data/` dizini altında, çalıştırılan kodların çıktıları yer almaktadır.

**twStart.py**
Twitter API'sine konfigurasyon değerlerine göre bağlanan ve bir Twitter nesnesi döndüren kütüphane modulü. Yardımcı metodlar da bu kod içindedir.

```python
import twStart
tw = twStart.hitTwitter()
```
kodu ile çağrılır.

**blockRTs.py**

Twitter API'sine bağlanıp, belirli bir tweet'i RT edenleri takipten çıkarmak ya da bloklamak için yazılmış deneme / sandbox kodu.

**muteWords.py**

Twitter API'sine bağlanıp, parametre olarak verilen text dosyasının içindeki kelimeleri, MUTED ya da UNMUTED durumuna geçiren deneme / sandbox kodu. 
__İLGİLİ TWITTER METODU OLMADIĞI İÇİN OBSOLETE DURUMDADIR__

**removeFollowed.py**

Twitter API'sine bağlanıp, takip edilenleri belirli kurallar çerçevesinde takipten çıkarmak için yazılmış deneme / sandbox kodu. İçindeki kurallar şu anda sadece en son tweet atılma tarihi ile, hesabın yaratılma tarihini kontrol etmektedir.

**twPlay.py**

Twitter API'sine bağlanıp, authenticate olmuş kullanıcının takipçi ve takip edilenler listesini almak için yazılmış deneme kodu.

**twSearch.py**

Twitter API'sine bağlanıp, verilen komut satırı parametrelerine göre tweetler içinde arama yapmak için yazılmış deneme / sandbox kodu.

**twStats.py**

UNDER CONSTRUCTION :)

**undoThanos.py**

Twitter API'sine bağlanıp, blokladığınız ve MUTE yaptığınız kullanıcıları listeleyen ve bunları geri almaya yarayan(UnBlock / UnMute) deneme / sandbox kodu.

**twThanos.py**

Twitter API'sine bağlanıp, takip edilen kullanıcılardan %50'sini takipten çıkarmak ya da bloklamak için yazılmış deneme / sandbox kodu.

## Çıktı dosyaları:

    followers_YYYYMMDD.txt          -> Takip edenler (twPlay.py)
    following_YYYYMMDD.txt          -> Takip edilenler (twPlay.py)
    RTBlocked_YYYYMMDD.txt          -> Bloklanmaya aday olanlar (blockRTs.py)
    twThanosDestroyed_YYYYMMDD.txt  -> %50'si block/mute yapılmış kullanıcıların listesi (twThanos.py)
    undoThanos_(M/B)_YYYYMMDD.txt   -> Unblok yapılmış / unmute edilmiş kullanıcıların listesi (undoThanos.py)

    Sonraki sürümlerde planlanan
    myStats_YYYYMMDD.txt    -> İstatistikler    (twMyStats.py) 

## Kaynaklar:

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
