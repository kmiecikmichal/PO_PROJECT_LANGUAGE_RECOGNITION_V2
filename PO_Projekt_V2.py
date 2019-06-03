import pickle
import re
from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.request import urlopen

def recognition():

    urladdress = "interia.pl"
    url = "http://" + urladdress

    try: html = urlopen(url).read()
    except URLError:
        return 

    soup = BeautifulSoup(html,"html.parser")
    w1 = soup.body.get_text().lower()
    w = re.sub(" +", " ", w1)

    all = ['a','b','c','d','e','f','g','h','i','j',
           'k','l','m','n','o','p','q','r','s','t',
           'u','v','w','x','y','z','ą','ä','à','â',
           'á','ć','ç','ę','é','è','ê','ë','æ','œ',
           'ï','î','í','ì','ł','ń','ñ','ó','ò','ô',
           'ö','ß','ś','ü','ù','û','ú','ÿ','ż','ź',' ',"'"]
   

    words = []
    for i in w:
        for j in all:
            if i == j:
                words.append(i)


    bigrams = []
    for i in range (len(words)-1):
                bigrams.append(words[i] + words[i+1])
  

    uniques = []
    for i in range (len(bigrams)):
        if bigrams[i] not in uniques:
            uniques.append(bigrams[i])
    
    
    values = []
    for i in range (len(uniques)):
        v = [uniques[i], bigrams.count(uniques[i])/len(bigrams)]
        values.append(v)
    
    
    letters = []
    for i in range (len(values)):
        for j in range (len(values[i])):
            if j == 1:
                letters.append(values[i][0])
    

    model_bigrams = []
    for i in all:
        for j in all:
            if not i == j == " ": #często się pojawiały 2 spacje
                model_bigrams.append(i + j)
    
    
    model_values = []
    for i in range (len(model_bigrams)):
        model_values.append([model_bigrams[i], 0])

    lan_big = letters
    lan_map = values
    mod_big = model_bigrams
    mod_map = model_values

    lan_big_new = []
    lan_map_new = []

    for i in range (len(lan_map)):
        if lan_big[i] in mod_big:
            lan_big_new.append(lan_big[i])
            lan_map_new.append(lan_map[i])

    for i in range (len(mod_map)):
        if mod_big[i] not in lan_big_new:
            lan_map_new.append(mod_map[i])

    map_txt = sorted(lan_map_new)
    

    with open("PolishBase.txt", "rb",) as pol:
        map_pol = pickle.load(pol)

    with open("EnglishBase.txt", "rb",) as eng:
        map_eng = pickle.load(eng)

    with open("FrenchBase.txt", "rb",) as fra:
        map_fra = pickle.load(fra)

    with open("SpanishBase.txt", "rb",) as esp:
        map_esp = pickle.load(esp)

    with open("GermanBase.txt", "rb",) as ger:
        map_ger = pickle.load(ger)

    with open("ItalianBase.txt", "rb",) as ita:
        map_ita = pickle.load(ita)


    err_pol, err_eng, err_fra, err_esp, err_ger, err_ita = 0, 0, 0, 0, 0, 0 

    for i in range(len(map_txt)):
        for j in range(len(map_txt[i])):
            if j == 1:
                err_pol += ((map_pol[i][j] - map_txt[i][j]) ** 2)
                err_eng += ((map_eng[i][j] - map_txt[i][j]) ** 2)
                err_fra += ((map_fra[i][j] - map_txt[i][j]) ** 2)
                err_esp += ((map_esp[i][j] - map_txt[i][j]) ** 2)
                err_ger += ((map_ger[i][j] - map_txt[i][j]) ** 2)
                err_ita += ((map_ita[i][j] - map_txt[i][j]) ** 2)

    print("pol ", err_pol)
    print("eng ", err_eng)
    print("fra ", err_fra)
    print("esp ", err_esp)
    print("ger ", err_ger)
    print("ita ", err_ita)
    

recognition()        
            








