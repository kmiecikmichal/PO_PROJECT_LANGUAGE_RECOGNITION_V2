#projekcik v2 tworzenie bazy danych- mapy bigramów 
import pickle

language = "Spanish"
with open(language + "Text.txt", encoding = "utf-8") as f:
    words = f.read().lower()
    words.split()


def lan_bigrams():

    bigrams = []
    for i in range (len(words)-1):
        bigrams.append(words[i] + words[i+1])

    return bigrams


def lan_counts():

    bigrams = lan_bigrams()

    counts = []
    for i in range (len(bigrams)):
        c = (bigrams.count(bigrams[i])/len(bigrams))
        counts.append(c)

    return counts


def lan_values():

    bigrams = lan_bigrams()
    counts = lan_counts()

    values = []
    for i in range (len(bigrams)):
        values.append([bigrams[i], counts[i]])

    return values


def lan_uniques():
    #zwraca mapę bigramów z bazy danych
    values = lan_values()

    uniques = []
    for i in range (len(values)):
        if values[i] not in uniques:
            uniques.append(values[i])

    return uniques


def lan_unique_bigrams():
    uniques = lan_uniques()

    literki = []
    for i in range (len(uniques)):
        for j in range (len(uniques[i])):
            if j == 1:
                literki.append(uniques[i][0])

    return literki


def mod_bigrams():

    all = ['a','b','c','d','e','f','g','h','i','j',
           'k','l','m','n','o','p','q','r','s','t',
           'u','v','w','x','y','z','ą','ä','à','â',
           'á','ć','ç','ę','é','è','ê','ë','æ','œ',
           'ï','î','í','ì','ł','ń','ñ','ó','ò','ô',
           'ö','ß','ś','ü','ù','û','ú','ÿ','ż','ź',' ',"'"]

    model_bigrams = []
    for i in all:
        for j in all:
            if not i == j == " ": #często się pojawiały 2 spacje
                model_bigrams.append(i + j)

    return model_bigrams


def mod_values():
    #zwraca mapę wszystkich bigramów
    model_bigrams = mod_bigrams()

    model_values = []
    for i in range (len(model_bigrams)):
        model_values.append([model_bigrams[i], 0])

    return model_values


def lang_map():
    
    lan_big = lan_unique_bigrams()
    lan_map = lan_uniques()

    mod_big = mod_bigrams()
    mod_map = mod_values()

    lan_big_new = []
    lan_map_new = []

    for i in range (len(lan_map)):
        if lan_big[i] in mod_big:
            lan_big_new.append(lan_big[i])
            lan_map_new.append(lan_map[i])

    for i in range (len(mod_map)):
        if mod_big[i] not in lan_big_new:
            lan_map_new.append(mod_map[i])

    language_map = sorted(lan_map_new)
    return language_map


language_map = lang_map()

#zapis
with open(language + "Base.txt", "wb") as w:
    pickle.dump(language_map, w)

#odczyt
with open(language + "Base.txt", "rb",) as f:
    b = pickle.load(f)

print(b)