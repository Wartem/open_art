import os.path
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from open_source import Source

cookies = {
    "incap_ses_275_1661977": "dCoOfWMCNGncFfpzeP/QA4If1GIAAAAAH5chfw8ftd2ccCkScCpoPQ==",
    #'PHPSESSID':'fjmr7plc0dmocm8roq7togcp92',
    "visid_incap_1661977": "zGu1zEBATdatObOPWOXc5nZczGIAAAAAQUIPAAAAAABO2YfMK/OgqNId+f9JQJp0",
    "_ga": "GA1.1.1619024324.1657560082",
    "_gid": "GA1.2.687656694.1657951080",
}


class MM(Source):
    """
    The Metropolitan Museum of Art open data source handler.
    """

    def __init__(self):
        self.source_org_file_name = "MetObjects.csv"
        self.res_csv_file_name = "mm_paintings.csv"
        self.objects = []

    def download_open_data(self):
        pass
        # self.download_zip_if_needed()

    def unpack_and_create_csv(self):
        pass
        # self.extract_zip_and_fix()

    def get_url_from_url_selenium(self, page_url: str):

        options = webdriver.ChromeOptions()
        options.binary_location = (
            "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
        )
        options.add_argument("--headless")
        options.add_argument("--ignore-certificate-errors-spki-list")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--test-type")
        options.add_argument("--log-level=3")
        chromeDriver = webdriver.Chrome(
            ChromeDriverManager().install(), options=options
        )

        chromeDriver.get(page_url)
        elem = chromeDriver.find_element(By.ID, "artwork__image")
        img_url = elem.get_attribute("src")
        return img_url

    def does_id_exist(self, id):
        df = pd.read_csv(
            self.res_csv_file_name,
            on_bad_lines="skip",
            index_col=False,
            dtype="unicode",
        )
        return df[id].any()

    def filter_update_fetch_fill_csv(self):

        if not os.path.exists(self.res_csv_file_name):
            with open(self.res_csv_file_name, "w"):
                pass

        df_filtered = pd.read_csv(
            self.source_org_file_name,
            on_bad_lines="skip",
            index_col=False,
            dtype="unicode",
        )

        painting_list = []
        columns = df_filtered.columns.to_list()

        for ind in df_filtered.index:

            if (
                df_filtered["Classification"][ind] == "Painting"
                and df_filtered["Is Public Domain"][ind] == "True"
            ):

                painting_list.append(df_filtered.iloc[ind])

        df_filtered = pd.DataFrame(painting_list, columns=columns)

        current_row_num = 0
        df_to_be_filled = pd.DataFrame()

        if os.path.getsize(self.res_csv_file_name):
            df_to_be_filled = pd.read_csv(
                self.res_csv_file_name,
                on_bad_lines="skip",
                index_col=False,
                dtype="unicode",
            )

        for ind in df_filtered.index:
            current_row_num += 1

            if (
                not df_to_be_filled.empty
                and df_filtered["Object ID"][ind] in df_to_be_filled["objectid"].values
            ):
                print(f"Skips obj {ind} already in csv")
                continue

            obj_list = []

            obj = {}
            obj["source"] = "MM"
            obj["objectid"] = str(df_filtered["Object ID"][ind]).strip()
            obj["title"] = str(df_filtered["Title"][ind]).strip()
            obj["attribution"] = str(df_filtered["Artist Display Name"][ind]).strip()
            obj["beginyear"] = str(df_filtered["Object Begin Date"][ind]).strip()
            obj["endyear"] = str(df_filtered["Object End Date"][ind]).strip()
            obj["displaydate"] = str(df_filtered["Title"][ind]).strip()
            obj["classification"] = str(df_filtered["Classification"][ind]).strip()
            obj["medium"] = str(df_filtered["Medium"][ind]).strip()
            obj["width"] = ""
            obj["height"] = ""

            img_ = ""

            try:
                resource = str(df_filtered["Link Resource"][ind]).strip()
                print(resource, "times:", current_row_num)
                img_ = self.get_url_from_url_selenium(resource)
            except:
                img_ = "link issue"
                continue

            obj["imgurl_thumb"] = img_
            obj["imgurl_downsized"] = img_
            obj["imgurl_full"] = img_

            obj_list.append(obj)

            df_save = pd.DataFrame(obj_list)
            if df_to_be_filled.empty:
                df_save.to_csv(self.res_csv_file_name, index=False, encoding="utf-8")
            else:
                df_save.to_csv(
                    self.res_csv_file_name,
                    mode="a",
                    header=False,
                    index=False,
                    encoding="utf-8",
                )


if __name__ == "__main__":
    mm = MM()
    mm.filter_update_fetch_fill_csv()
