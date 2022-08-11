import os
from bs4 import BeautifulSoup
import pandas as pd
import requests

cookies = {
    'incap_ses_727_1662004':'ye/2Wcp8qxn7ONPvT9MWCiOu02IAAAAAAhqTpHPORGccs5t0YuyKwQ==', 
    #'PHPSESSID':'fjmr7plc0dmocm8roq7togcp92', 
    'visid_incap_1661977':'zGu1zEBATdatObOPWOXc5nZczGIAAAAAQUIPAAAAAABO2YfMK/OgqNId+f9JQJp0', 
    '_ga':'GA1.2.1619024324.1657560082', 
    '_gid':"GA1.2.687656694.1657951080"
}

def get_image_url(page_url: str) -> str:
    
    reponse = requests.get(page_url, cookies=cookies)

    if reponse.ok:
        soup = BeautifulSoup(reponse.text, "html.parser")
        img_ = soup.find("img", {"class": "artwork__image"})
        
        if img_:
            return str(img_['src'])
        return ""
        #print(soup.find(class_="artwork__image").src)
        #os.system("pause")

def fix_met_objects_csv():
    file = "MetObjects.csv"

    df = pd.read_csv(file, on_bad_lines='skip', index_col=False, dtype='unicode')

    painting_list = []
    columns = df.columns.to_list()

    for ind in df.index:
        if(df['Classification'][ind] == "Paintings" 
        and df['Is Public Domain'][ind] == "True"):

            painting_list.append(df.iloc[ind])
            # Progress
            if(ind % 50000 == 0):
                print(ind)
            
    try:
        pass
        df = pd.DataFrame(painting_list, columns=columns)
        for ind in df.index:
            "http://www.metmuseum.org/art/collection/search/" + df['Object ID'][ind]
        df.to_csv('mm_paintings.csv', index=False, encoding='utf-8')
        #df.to_csv("Classification.csv", encoding='utf-8', on_bad_lines='skip')
    except KeyError:
            pass


if __name__ == "__main__":
    get_image_url("https://www.metmuseum.org/art/collection/search/35973")

def _main_old():

    file = "MetObjects.csv"

    df = pd.read_csv(file, on_bad_lines='skip', index_col=False, dtype='unicode')

    painting_list = []
    columns = df.columns.to_list()
    #painting_df = ""

    for ind in df.index:
        if(df['Classification'][ind] == "Paintings" 
        and df['Is Public Domain'][ind] == "True"):
            #Object ID

            painting_list.append(df.iloc[ind])
            if(ind % 50000 == 0):
                print(ind)
            try:
                pass
                #df.drop(df.iloc[ind])
            except KeyError:
                pass
            
    #print(len(painting_list))

    #print(painting_list[1])

    try:
        pass
        df = pd.DataFrame(painting_list, columns=columns)
        for ind in df.index:
            "http://www.metmuseum.org/art/collection/search/" + df['Object ID'][ind]
        df.to_csv('mm_paintings.csv', index=False, encoding='utf-8')
        #df.to_csv("Classification.csv", encoding='utf-8', on_bad_lines='skip')
    except KeyError:
            pass

    """ with open('mm_paintings.csv', 'w+', encoding="utf-8") as f:
        for painting in painting_list:
            f.write(painting + "\n") """
    