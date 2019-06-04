import pickle
import re

language = ""
with open(language + "Text.txt") as f:
    w = f.read().lower().split
    w2 = re.sub(r"([^abcdefghijklmnopqrstuvwxyząäàâáćçęéèêëæœïîíìłńñóòôößśüùûúÿżź '])", " ", w)
    words = re.sub(" +", " ", w2)


all = ['a','b','c','d','e','f','g','h','i','j',
       'k','l','m','n','o','p','q','r','s','t',
       'u','v','w','x','y','z','ą','ä','à','â',
       'á','ć','ç','ę','é','è','ê','ë','æ','œ',
       'ï','î','í','ì','ł','ń','ñ','ó','ò','ô',
       'ö','ß','ś','ü','ù','û','ú','ÿ','ż','ź',' ',"'"]


mod_bigrams = []
for i in all:
    for j in all:
        if not i == j == " ": #często się pojawiały 2 spacje
             mod_bigrams.append(i + j)


map_mod = dict()
for k in mod_bigrams:
        map_mod[k] = 0


bigrams = []
for i in range (len(words)-1):
        bigrams.append(words[i] + words[i+1])


map_bigrams = dict()
for k in bigrams:
    if not k in map_bigrams:
        map_bigrams[k] = 1/len(bigrams)
    else:
        map_bigrams[k] += 1/len(bigrams)

map_mod.update(map_bigrams)


#zapis
with open(language + "Base.txt", "wb") as w:
        pickle.dump(map_mod, w)

#odczyt
with open(language + "Base.txt", "rb",) as f:
    b = pickle.load(f)

print(b)