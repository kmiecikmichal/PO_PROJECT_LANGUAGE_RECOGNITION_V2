import os
import re
import pickle
import matplotlib
import matplotlib.pyplot as plt
from tkinter import *
from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.request import urlopen
import time as t



def recognition():

    start = t.time()

    try: os.remove("plot.png")
    except: pass

    urladdress = e1.get()
    url = "http://" + urladdress

    try: html = urlopen(url).read()
    except URLError:
        l1.place_forget()
        l4.config(text = "Page not found")
        master.minsize(540,274)
        return 

    
    soup = BeautifulSoup(html,"html.parser")
    w = ""
    a_tags = soup.find_all('a')
    for a in a_tags:
        w = w + a.text.lower()
    w2 = re.sub(r"([^abcdefghijklmnopqrstuvwxyząäàâáćçęéèêëæœïîíìłńñóòôößśüùûúÿżź '])", "  ", w)
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


    err_pol, err_eng, err_fra, err_ger, err_ita, err_esp = 0, 0, 0, 0, 0, 0 
    
    for values in map_mod:
        err_pol += ((map_mod[values] - map_pol[values]) ** 2)
        err_eng += ((map_mod[values] - map_eng[values]) ** 2)
        err_fra += ((map_mod[values] - map_fra[values]) ** 2)
        err_ger += ((map_mod[values] - map_ger[values]) ** 2)
        err_ita += ((map_mod[values] - map_ita[values]) ** 2)
        err_esp += ((map_mod[values] - map_esp[values]) ** 2)


    if   len(words) > 10:
          
         try: plt.clf()
         except: pass

         hist_lan = ("POL","ENG","FRA","GER","ITA","ESP")
         hist_val = (err_pol,err_eng,err_fra,err_ger,err_ita,err_esp)

         plt.bar(hist_lan, hist_val)
         plt.title("Error of language map similarity")
         plt.ylabel("Error")
         plt.savefig("plot.png")


    if   len(words) <= 10:
         lang = "No language in the database or insufficient data"

    elif err_pol < err_eng and err_pol < err_fra and err_pol < err_esp and err_pol < err_ger and err_pol < err_ita:
         lang = "Polish language"

    elif err_eng < err_pol and err_eng < err_fra and err_eng < err_esp and err_eng < err_ger and err_eng < err_ita:
         lang = "English language"

    elif err_fra < err_eng and err_fra < err_pol and err_fra < err_esp and err_fra < err_ger and err_fra < err_ita:
         lang = "French language"
    
    elif err_ger < err_eng and err_ger < err_fra and err_ger < err_esp and err_ger < err_pol and err_ger < err_ita:
         lang = "German language"

    elif err_ita < err_eng and err_ita < err_fra and err_ita < err_esp and err_ita < err_ger and err_ita < err_pol:
         lang = "Italian language"

    elif err_esp < err_eng and err_esp < err_fra and err_esp < err_pol and err_esp < err_ger and err_esp < err_ita:
         lang = "Spanish language"

    else:
         lang = "No language in the database or insufficient data"

    end = t.time()
    elapsed_time = round((end - start),5)

    try:
        photo = PhotoImage(file = "plot.png")
        l1.config(image = photo)
        l1.image = photo
        l1.place(x = 540, y = 20)
        master.minsize(1200, 520)
    except:
        l1.place_forget()
        master.minsize(540, 274)

    l4.config(text = lang)
    l5.config(text = ("elapsed time ", elapsed_time, "s"))

    

master = Tk()
master.minsize(540,274)
master.configure(bg = "gray30")
master.title("Language recognition")


l1 = Label(master)


l2 = Label(master, 
           text  = "Website Address: ", 
           bg    = "gray30", 
           fg    = "white", 
           font  = ("Verdana", 14))
l2.place(x = 20, y = 10, width = 500, height = 64)


e1 = Entry(master,  
           fg    = "gray20", 
           font  = ("Verdana", 14))
e1.place(x = 20, y = 70, width = 500, height = 28)


l3 = Label(master, 
           text  = "Language:", 
           bg    = "gray30", 
           fg    = "white", 
           font  = ("Verdana", 14))
l3.place(x = 20, y = 118, width = 500, height = 64)


l4 = Label(master, 
           text  = "", 
           bg    = "white", 
           fg    = "gray20", 
           font  = ("Verdana",14))
l4.place(x = 20, y = 178, width = 500, height = 28)


l5 = Label(master, 
           text  = "", 
           bg    = "gray30", 
           fg    = "white", 
           font  = ("Verdana",8))
l5.place(x = 20, y = 480, height = 20)


b1 = Button(master, 
            text    = "Quit",
            command = master.quit, 
            bg      = "white", 
            fg      = "gray20", 
            font    = ("Verdana",12))
b1.place(x = 20, y = 226, width = 60, height = 28)


b2 = Button(master, 
            text    = "Recognize", 
            command = recognition, 
            bg      = "white", 
            fg      = "gray20", 
            font    = ("Verdana",12))
b2.place(x = 400, y = 226, width = 120, height = 28)


mainloop( )   