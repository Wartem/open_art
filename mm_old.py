import time
import os.path
import pandas as pd
import requests
from bs4 import BeautifulSoup
from open_source import Source
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

cookies = {
    'incap_ses_275_1661977':'dCoOfWMCNGncFfpzeP/QA4If1GIAAAAAH5chfw8ftd2ccCkScCpoPQ==', 
    #'PHPSESSID':'fjmr7plc0dmocm8roq7togcp92', 
    'visid_incap_1661977':'zGu1zEBATdatObOPWOXc5nZczGIAAAAAQUIPAAAAAABO2YfMK/OgqNId+f9JQJp0', 
    '_ga':'GA1.1.1619024324.1657560082', 
    '_gid':"GA1.2.687656694.1657951080"
}

class MM(Source):
    
    def __init__(self):
        self.source_org_file_name = "MetObjects.csv"
        self.csv_file_name = "mm_paintings.csv"
        self.objects = []
    
    def download_open_data(self):
        pass
        # self.download_zip_if_needed()

    def unpack_and_create_csv(self):
        pass
        # self.extract_zip_and_fix()
        
    def get_url_from_url_selenium(self, page_url: str):
        
        options = webdriver.ChromeOptions()
        options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
        options.add_argument("--window-size=800,600")
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--test-type')
        options.add_argument('log-level=3')
        chromeDriver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
        
        chromeDriver.get(page_url)
        elem = chromeDriver.find_element(By.ID, "artwork__image")
        img_url =  elem.get_attribute("src")
        #print(img_url)
        return img_url
        
    def _get_image_url_from_url(self, page_url: str) -> str:
        time.sleep(0.1)
        reponse = requests.get(page_url, cookies=cookies)
        print(page_url)
        
        if reponse.ok:
            soup = BeautifulSoup(reponse.text, "html.parser")
            print(soup)
            img_ = soup.findAll("img", {"class": "artwork__image"})
            
            print(img_)
            
            if img_:
                img_ = img_[0]
                src = str(img_['src'])
                print(src)
                return src
            return ""
        
    def _get_image_url_from_row(self, df, index):
        return self.get_image_url_from_url("http://www.metmuseum.org/art/collection/search/" + df['Object ID'][index])

    def does_id_exist(self, id):
        df = pd.read_csv(self.csv_file_name, on_bad_lines='skip', \
            index_col=False, dtype='unicode')
        return df[id].any()
            
    
    def fix_met_objects_csv(self):
        
        if not os.path.exists(self.csv_file_name):
            with open(self.csv_file_name, "w"):
                pass

        df = pd.read_csv(self.source_org_file_name, on_bad_lines='skip', \
            index_col=False, dtype='unicode')

        painting_list = []
        columns = df.columns.to_list()

        for ind in df.index:
           
            if(df['Classification'][ind] == "Paintings" 
            and df['Is Public Domain'][ind] == "True"):

                painting_list.append(df.iloc[ind])
                # Progress
                if(ind % 50000 == 0):
                    print(ind)
                
        df = pd.DataFrame(painting_list, columns=columns)
            # rows
            
        
        
        times = 0
        
        old_df = pd.DataFrame()
        
        if(os.path.getsize(self.csv_file_name)):
            old_df = pd.read_csv(self.csv_file_name, on_bad_lines='skip', \
                index_col=False, dtype='unicode')
        
        for ind in df.index:
            times += 1
            
            # print("ind", ind)
            if not old_df.empty and df['Object ID'][ind] in old_df['objectid'].values: #old_df['objectid'][ind].any():
                print(f"Skips obj {ind} already in csv")
                continue
            
            obj_list = []
            
            obj = {}
            obj["source"] = "MM"
            obj["objectid"] = str(df['Object ID'][ind]).strip()
            obj["title"] = str(df['Title'][ind]).strip()
            obj["attribution"] = str(df['Artist Display Name'][ind]).strip()
            obj["beginyear"] = str(df['Object Begin Date'][ind]).strip()
            obj["endyear"] = str(df['Object End Date'][ind]).strip()
            obj["displaydate"] = str(df['Title'][ind]).strip()
            obj["classification"] = str(df['Classification'][ind]).strip()
            obj["medium"] = str(df['Medium'][ind]).strip()
            obj["width"] = ""
            obj["height"] = ""
            
            img_ = ""
            
            try:
                resource = str(df['Link Resource'][ind]).strip()
                print(resource, "times:", times)
                img_ = self.get_url_from_url_selenium(resource)
            except:
                img_ = "link issue"
                continue
            
            obj["imgurl_thumb"] = img_
            obj["imgurl_downsized"] = img_
            obj["imgurl_full"] = img_
            
            obj_list.append(obj)
    
            df_save = pd.DataFrame(obj_list)
            if old_df.empty:
                df_save.to_csv(self.csv_file_name, index=False, encoding='utf-8')
            else:
                df_save.to_csv(self.csv_file_name, mode='a', header=False, index=False, encoding='utf-8')
            if times % 10 == 0:
                pass


if __name__ == '__main__':
    mm = MM()
    mm.fix_met_objects_csv()
            
            
            