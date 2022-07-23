
import csv
import io
import os
import requests
import pandas as pd
import wget
import re

#url = "https://github.com/MuseumofModernArt/collection/archive/refs/heads/master.zip"

#url = "https://github.com/MuseumofModernArt/collection/blob/master/Artworks.csv"

#file = wget.download(url, "/downloads")

#s=requests.get(url).content
#df = pd.read_csv(file, on_bad_lines='skip', index_col=False, dtype='unicode')

#outname = 'MuseumofModernArt.csv'

#outdir = ''

#if not os.path.exists(outdir):
    #os.mkdir(outdir)
    
#fullname = os.path.join(outdir, outname)  

#df.to_csv(outname)

file = "artworksModerna.csv"

df = pd.read_csv(file, on_bad_lines='skip', index_col=False, dtype='unicode')

print(df.columns)
print(df[:1])
#for i, row in enumerate(df):
#rint("df.iloc[[5]]", df.iloc[[5]])
    #print(row)
    
row = df.iloc[1000]   
    
ObjectID = row.loc['ObjectID']
URL = row.loc['URL']
ThumbnailURL = row.loc['ThumbnailURL']
print(ObjectID, URL, ThumbnailURL, sep="\n")

