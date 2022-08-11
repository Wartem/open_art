import csv
import io
import requests
import pandas as pd
import wget
import re


final_ok_paintings = ["acrylic","drawing","drawings","fresco","gouache","monopainting","oil","paint","painted","painting","palisander","panel","sandalwood","sandstone","tempera"]

file = "MetObjects.csv"

df = pd.read_csv(file, on_bad_lines='skip', index_col=False, dtype='unicode')

medium_list = []

for ind in df.index:
    
    for final in final_ok_paintings:
        if str(df['Medium'][ind]).find(final) != -1:
            medium_list.append(df['Medium'][ind])
            
print(len(medium_list))
medium_list = list(map(str, medium_list))
print(len(medium_list))
medium_list = list(filter(lambda x: " " not in str(x), medium_list))
print(len(medium_list))
medium_list = list(filter(lambda x: re.match(r"^\w+(?:-*)(?:\w*)$", x), medium_list))
print(len(medium_list))
medium_list = list(set(medium_list))
print(len(medium_list))
medium_list.sort()

print(medium_list)
print(len(medium_list))