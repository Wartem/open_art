import csv
import io
import requests
import pandas as pd
import wget
import re

""" from translate import Translator
from googletrans import Translator """

#translator= Translator(to_lang="German")

file = "MetObjects.csv"

df = pd.read_csv(file, on_bad_lines='skip', index_col=False, dtype='unicode')

#print(df.columns)

classifications = df["Classification"]

classifications = list(map(str, (set(classifications))))
#classifications.sort()

#lamdafun = lambda x: re.split("\w+(?:-*)(?:\w*)", x)[0]

#classifications = list(map(lamdafun, classifications))

classifications_res = []

for cl in classifications:
    
    #cl = re.split("\w+(?:-*)(?:\w*)", cl)
    
    cl = re.split("\W", cl)[0].capitalize()
    
    classifications_res.append(cl)
    #print(cl)
    #print(len(cl)) 
#print(classifications)



classifications_res = list(set(classifications_res))
classifications_res.sort()

""" translator = Translator(to_lang="Swedish")

translater = lambda x: translator.translate(x)

translator.translate("Good Morning!")

print(translation) """

with open('classifications.txt', 'w+', encoding="utf-8") as f:
    for classific in classifications_res:
        f.write(classific.strip() + "\n")

""" text = 'This site is awesome'
from googletrans import Translator

translator = Translator()
translator.translate(text , dest ='sw').text
print() """
