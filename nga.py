import datetime
import shutil
import sys
from zipfile import ZipFile
import wget
import os.path
import pandas as pd
import glob
import requests
from bs4 import BeautifulSoup

from a_constants import *
from csv_info import get_file_creation_date
from csv_info import get_month_name_from_int
from a_constants import Constants as Const

from open_source import Source
from nga_open_object import Object


class NGA(Source):
    
    def __init__(self):
        self.objects = []
        
        # TODO: remove_old_and_create_new_sqlite_db()

    def download_open_data(self):
        self.download_zip_if_needed()

    def unpack_and_create_csv(self):
        self.extract_zip_and_fix()

    @staticmethod
    def get_nga_latest_remote_git_update_date():
        # TODO: Add SSL:
        # Ignore SSL Certificate errors
        # ctx = ssl.create_default_context()
        # ctx.check_hostname = False
        # ctx.verify_mode = ssl.CERT_NONE

        url = "https://github.com/NationalGalleryOfArt/opendata/commits/main"
        data = requests.get(url)

        html = BeautifulSoup(data.text, "html.parser")
        timeline = html.find(class_="TimelineItem-body").h2.text
        d_str = timeline.split("Commits on ")[1]

        year = int(d_str[-4:])
        month = int(Constants.months_abbreviated[d_str[0:3]])
        day = int(d_str.split(",")[0].split(" ")[1])
        date = datetime.datetime(year, month, day)
        return date

    def is_nga_file_update_needed(self):
        git_date = self.get_nga_latest_remote_git_update_date()
        file_date = get_file_creation_date(Constants.NGA_ZIP_FILE_PATH)
        if git_date > file_date:
            print("A seemingly newer version is available for " +
                  Const.NGA_REMOTE_DATA_ZIP)
        else:
            print(
                "Your file is up to date. No need to download again from\n",
                Const.NGA_REMOTE_DATA_ZIP,
            )

        print(
            "File on server was uploaded:",
            git_date.year,
            get_month_name_from_int(
                Constants.months_abbreviated, git_date.month),
            git_date.day,
            "\nYour downloaded local file ("
            + Constants.DOWNLOAD_FOLDER
            + Const.NGA_ZIP_FILE_NAME
            + ") is from:",
            file_date.year,
            get_month_name_from_int(
                Constants.months_abbreviated, file_date.month),
            file_date.day,
        )

    def download_zip_if_needed(self):
        if os.path.exists(Constants.NGA_ZIP_FILE_PATH):
            self.is_nga_file_update_needed()
            if input("Remove and replace the existing file? yes/no ") == "yes":
                if os.path.exists(Constants.NGA_ZIP_FILE_PATH):
                    os.remove(Constants.NGA_ZIP_FILE_PATH)
                    print("Old file removed.")

                self.download_zip(
                    Const.NGA_REMOTE_DATA_ZIP, Constants.DOWNLOAD_FOLDER
                )
                if input(
                        f"Extract the downloaded {Const.NGA_ZIP_FILE_NAME} \
                        and create/replace the database? \n yes/no ") == "yes":
                    self.extract_zip_and_fix()
        else:
            print("No file found. Downloading...")
            self.download_zip(
                Const.NGA_REMOTE_DATA_ZIP, Constants.DOWNLOAD_FOLDER
            )
            self.extract_zip_and_fix()

    @staticmethod
    def drop_unwanted_columns(df: pd.DataFrame):
        for col in df.columns:
            if col not in Const.COLUMNS_USED:
                df.drop(col, axis=1, inplace=True)
        return df

    

    #def add_fixed_urls(self, df):
        
        #temp = [] 
        
        #for index, row in df.iterrows():
            
            
    
            #return df
    
        """ nga_object = Object(row["source"][index],
        row["objectid"][index],
        row["title"][index],
        row["attribution"][index],
        row["beginyear"][index],
        row["endyear"][index],
        row["displaydate"][index],
        row["classification"][index],
        row["medium"][index],
        row["width"][index],
        row["height"][index], 
        row["iiifurl"][index]) """
        
        #temp.append(nga_object)

        # Generated inside Object constructor
        """ full_url
        imgurl_downsized
        imgurl_thumb """
        
        
    def fix_image_properties(self, df: pd.DataFrame):
    
        for index, row in df.iterrows():
            # print(row["width"][index])
            width = int(df["width"][index])
            height = int(df["height"][index])
            iiifurl = str(df["iiifurl"][index])
            
            # print("width etc ", width, height, iiifurl)
            
            imgurl_full = ""
            imgurl_downsized = ""
            imgurl_thumb = ""

            if width > 4096 or height > 4096:
                if width > 4096:
                    width = 4096

                if height > 4096:
                    height = 4096

                imgurl_full = f"{iiifurl}/full/!{str(width)},{str(height)}/0/default.jpg"
            else:
                imgurl_full = f"{iiifurl}/full/{str(width)},{str(height)}/0/default.jpg"

            if height > 1500 or width > 1500:
                imgurl_downsized = iiifurl + "/full/!1500,1500/0/default.jpg"
            else:
                imgurl_downsized = iiifurl + f"/full/!{str(width)},{str(height)}/0/default.jpg"
            
            imgurl_thumb = iiifurl + "/full/!200,200/0/default.jpg"
                
            df.at[index, "source"] =  "NGA"
            df.at[index, "imgurl_thumb"]=  imgurl_thumb
            df.at[index, "imgurl_downsized"]= imgurl_downsized
            df.at[index, "imgurl_full"] = imgurl_full
            
            #df.get_index()
            #df.insert(0, 'source', 'NGA')
            
            #df.assign('full_urlthumb', imgurl_thumb)
            #df.assign('full_urldownsized', imgurl_downsized)
            #df.assign('full_url', full_url)
            
        return df
    
    def merge(self, csv1_file_name, csv2_file_name):
        # reading two csv files
        df1 = pd.read_csv(csv1_file_name, on_bad_lines='skip', index_col=False, dtype='unicode')
        df2 = pd.read_csv(csv2_file_name, on_bad_lines='skip', index_col=False, dtype='unicode')

        df1 = self.drop_unwanted_columns(df1)
        df2 = self.drop_unwanted_columns(df2)

        res = pd.merge(df1, df2,
                       on=['objectid'],
                       how='inner')
        
        res = self.fix_image_properties(res)  # fix_image_properties()
        
        res.drop('iiifurl', inplace=True, axis=1)
        
        res.to_csv(csv1_file_name, index=False)
        if os.path.exists(csv2_file_name):
            os.remove(csv2_file_name)
            
        return csv1_file_name

    def fix_nga_csv_in_folder(self, art_folder):
        csv_file_names = glob.glob(os.path.join(art_folder, "*.csv"))
        # drop_unwanted_columns_in_published_images("opendata-main/data/published_images.csv")
        # drop_unwanted_columns_in_objects(NGA_CSV_CONTAINER + "\\objects.csv")
        # drop_unwanted_columns_in_published_images(NGA_CSV_CONTAINER + "\\published_images.csv")

        # Prepare merge objects.csv with published_images.csv
        for file in csv_file_names:
            end_part = file.split("\\")
            end_part = end_part[len(end_part) - 1]

            if "published_images.csv" in end_part:
                df = pd.read_csv(file, on_bad_lines='skip', index_col=False,
                                 dtype='unicode')
                df.rename(columns={'depictstmsobjectid': 'objectid'}, inplace=True)
                df.to_csv(file)
                # if end_part not in files_used:
                # os.remove(file)
                # if "objects.csv" in csv_file_names and "published_images.csv" in csv_file_names:
        print("Merging", Const.NGA_CSV_CONTAINER + "\\objects.csv", "with",
              Const.NGA_CSV_CONTAINER + "\\published_images.csv")
        # Merging
        self.merge(Const.NGA_CSV_CONTAINER + "\\objects.csv",
                   Const.NGA_CSV_CONTAINER + "\\published_images.csv")

    def extract_zip_and_fix(self):
        
        if os.path.exists(Constants.NGA_ZIP_FILE_PATH):
            print(Constants.NGA_ZIP_FILE_PATH)
            if os.path.exists(Const.NGA_FOLDER_RENAME_TO):
                shutil.rmtree(Const.NGA_FOLDER_RENAME_TO)
            
            with ZipFile(Constants.NGA_ZIP_FILE_PATH, "r") as zip_f:
                zip_f.printdir()
                print("Extract start...")

                for file in zip_f.namelist():
                    if file.startswith(Const.NGA_DOWNLOAD_STARTS_WITH):

                        end_part = file.split("data/")
                        end_part = end_part[len(end_part) - 1]
                        # print(end_part)
                        if end_part in Const.FILES_USED:
                            zip_f.extract(file, Const.NGA_FOLDER_RENAME_TO)

                if zip_f.namelist():
                    os.rename(Const.NGA_CSV_DIR + Const.NGA_FOLDER_TO_RENAME, Const.NGA_FOLDER_RENAME_TO)
                    print("Now cleaning up the files in", Const.NGA_CSV_CONTAINER)
                    self.fix_nga_csv_in_folder(Const.NGA_CSV_CONTAINER)
                    print("Extract complete!")
                else:
                    print("Extract failed.")

    @staticmethod
    def download_zip(data_url, download_folder):
        print(f"Downloading from {data_url} ...")
        try:
            file = wget.download(data_url, download_folder, bar=bar_progress)
            print("Download complete for " + file)
        except FileNotFoundError:
            print("File Not Found Error occurred.")
        except PermissionError:
            print("Permission issue: Make sure files are not already in use.")


def bar_progress(current, total, width=80):
    progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    # Don't use print() as it will print in new line every time.
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


if __name__ == "__main__":
    print("No main. Call functions instead.")
