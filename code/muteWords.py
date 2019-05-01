'''
Author: Tolga MIRMIRIK (@mirmirik)

Twitter API'sine bağlanıp, parametre olarak verilen text dosyasın içindeki kelimeleri, MUTED ya da UNMUTED 
durumuna geçiren deneme / sandbox kodu. Kullanmak için, myTwitter.cfg dosyası içine ilgili değerlerin eklenmesi gerekmektedir.

Konfigürasyon dosyası değerleri:
    [auth]
    ACCOUNT = <bilgilerine erişilecek size ait hesap adı>
    CONSUMER_KEY = <Twitter Development / APPS kısmından alınacak olacan CONSUMER KEY>
    CONSUMER_SECRET = <Twitter Development / APPS kısmından alınacak olacan CONSUMER SECRET>

Komut satırından çalıştırma:
    python muteWords.py 
        -f <File name>      : İçinde MUTE edilmesi ya da -u parametresine bağlı olarak UNMUTE edilmesi istenilen kelimelerin
                                bulunduğu dosya adı
        -u <True / False>   : Eğer "-u True" ise, dosya içindeki kelimeler UNMUTE edilir, False ise MUTE. Varsayılan değer = False.

Twitter API'ye erişim sağlayan wrapper library:
    https://github.com/sixohsix/twitter

Geliştiriciler için kullanıcı ve hesap bilgilerinin kullanımı :
    https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/overview
'''

import twStart
import argparse
import os
from colorama import Fore, Back, Style, init

def muteWords(FileName, Unmute):

    message = "Kelimeler MUTE listesin" 
    message += "den çıkarılacak!" if Unmute else "e eklenecek!"

    color = Fore.RED if Unmute else Fore.GREEN

    if not (os.path.isfile(FileName)):
        return
    else:
        # tw = twStart.hitTwitter()
        try:
            f=open(FileName, "r")
            wordsToProcess = f.readlines()
            for word in wordsToProcess:
                print(Style.BRIGHT + color + "\t" + word.replace("\n",""))
            print(message + "\nEmin misiniz?")

            if (input("[E]vet / [H]ayır: ") == "E"):
                for word in wordsToProcess:
                    ''' 
                    Bir gün umarım ki "muted keywords" listesine kelime eklemek ya da çıkarmak için bir method açılır Twitter API için :( 
                    Eğer olursa, tam burada, o method'u çağırmak için gerekli çağrı olmalı. Şunun gibi bir şey iş görecektir:

                    if (UnMute):
                        tw.MutedWords.Destroy(word)
                    else:
                        tw.MutedWords.Add(word)

                    '''
                    print(Style.BRIGHT + color + "\t" +word.replace("\n","") + " ✅....")

                print("Kelimelerin durumları, listede güncellendi! Çıkarılması gerekenler çıktı, eklenmesi gerekenler eklendi. Her şey olması gerektiği gibi...")
        except:
            print ("Bir şeyler çok yanlış gitti ama ne oldu anlayamadım. Sonraki commit'te detaylı bilgi vereceğim... (umarım)")

def main():
    parser = argparse.ArgumentParser(description="Parametre olarak verilen dosyadaki kelimeleri, Twitter hesabınızda MUTE/UNMUTE etmeye yarar.")
    parser.add_argument("-f",
                        dest="FILE_NAME",
                        help="İçinde, her bir satırda MUTE/UNMUTE edilecek kelimelerin bulunduğu dosya ismi. kelimeler CR/LF ile ayrılmalıldır.")
    parser.add_argument("-u",
                        dest="UNMUTE",
                        help="Eğer True ise, dosya içindeki kelimeler MUTE statüsünden kaldırılır. Varsayılan olarak False kullanılmaktadır.",
                        default=False)

    args = parser.parse_args()
    if args.FILE_NAME:
        muteWords(args.FILE_NAME, args.UNMUTE)
    else:
        print("\nLütfen işlem yapılacak kelimelerin bulunduğu dosyayı belirtmek için -f parametresini kullanınız.\n")

if __name__ == "__main__":
    init(autoreset=True)
    main()
