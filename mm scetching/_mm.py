
import csv
import io
import requests
import pandas as pd
import wget
import re

final_ok_paintings = ["acrylic","drawing","drawings","fresco","gouache","monopainting","oil","paint","painted","painting","palisander","panel","sandalwood","sandstone","tempera"]

ok_paintings = ["acrylic","oil","paint","acrylic","drawing","decorative","action","painting","aerial","anamorphosis","camaieu","casein","chiaroscuro","divisionism","easel","encaustic","foreshortening","fresco","gouache","graffiti","grisaille","impasto","miniaturepainting","mural","oilpainting","panel","panorama","perspective","plein","sand","scroll","sfumato","sgraffito","sottoinsu","tachism","tempera","tenebrism","trompl’oeil"]

#MM_CSV_URL = "https://github.com/metmuseum/openaccess/blob/master/MetObjects.csv"

#file = wget.download(MM_CSV_URL)

# s=requests.get(MM_CSV_URL).content
#df = pd.read_csv(file, on_bad_lines='skip', index_col=False, dtype='unicode')
# df.to_csv('metmuseum.csv')

file = "MetObjects.csv"

df = pd.read_csv(file, on_bad_lines='skip', index_col=False, dtype='unicode')
#df = df.query('Is Public Domain == TRUE')

medium_list = []

for ind in df.index:
    medium_list.append(df['Medium'][ind])

medium_list = list(map(str, medium_list))
# medium_list = list(map(lambda x: str(x).split(" ")[0], medium_list)
medium_list = filter(lambda x: " " not in str(x), medium_list)
medium_set = set(medium_list)
medium_list = list(map(str, medium_set))
medium_list.sort()

with open('mediums.txt', 'w+', encoding="utf-8") as f:
    
    # OK format values in list from DB 
    ok_from_db = list(filter(lambda x: re.match(r"^\w+(?:-*)(?:\w*)$", x), medium_list))
    # OK format list set as lower case (from manual filter through)
    ok_from_db = list(map(str.lower, ok_from_db))
    # Filter all from database corresponding to something in the manual list
    # medium_filtered = list(filter(lambda x: re.search(x.lower(), *[e for e in ok_paintings_lower]), ok_from_db))
    
    # print(ok_from_db)
    
    medium_ok_list = []
    
    for medium in ok_from_db:
        #found_medium = bool(filter(lambda x: re.search(x.lower(), medium), ok_painting))
        for ok_paint in ok_paintings:
            ok_paint = ok_paint.strip()
            medium = medium.strip()
            
            if medium.find(ok_paint) != -1:
                medium_ok_list.append(medium)
    
    medium_ok_list = list(set(medium_ok_list))
    medium_ok_list.sort()
    for medium in medium_ok_list:
        f.write(medium + "\n")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # print(medium)
        #ok = bool(re.match(r"[a-zA-Z](?:[^.,?!]+)", medium))
        # ok = bool(re.match(r"^\w+(?:-*)(?:\w*)$", medium))
        #string = medium.replace('?','').replace('.','').replace(',','').replace(' ','').replace('\\', '')
        
        # ok_paintings_lower = list(map(str.lower, ok_painting))
        
        # medium_filtered = list(filter(lambda x: re.search(x.lower, ok_paintings_lower), medium_list))
        
        # if(ok and len(medium) > 1 and 
           # bool(re.search(medium.lower(), list(map(str.lower, ok_painting))))
           # ):
           #  f.write(medium + "\n")

#print(medium for medium in medium_list)
# print(len(medium_set))
#li = list(map(str,list(set(li)))).sort()

# print(medium_set)


# print(df.columns)
# print(df.at[5])
