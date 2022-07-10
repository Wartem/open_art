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
from open_sqlite_handling import remove_old_and_create_new_sqlite_db
from csv_info import get_file_creation_date
from csv_info import get_month_name_from_int
from a_constants import Constants as Const

from open_source import Source


class NGA(Source):

    def download_open_data(self):
        self.download_zip_if_needed()

    def unpack_and_recreate_db(self):
        self.extract_zip_and_recreate_db()

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
            print("A seemingly newer version is available for " + Const.NGA_REMOTE_DATA_ZIP)
        else:
            print(
                "Your file is up to date. No need to download again from\n",
                Const.NGA_REMOTE_DATA_ZIP,
            )

        print(
            "File on server was uploaded:",
            git_date.year,
            get_month_name_from_int(Constants.months_abbreviated, git_date.month),
            git_date.day,
            "\nYour downloaded local file ("
            + Constants.DOWNLOAD_FOLDER
            + Const.NGA_ZIP_FILE_NAME
            + ") is from:",
            file_date.year,
            get_month_name_from_int(Constants.months_abbreviated, file_date.month),
            file_date.day,
        )

    def extract_zip_and_recreate_db(self):
        if os.path.exists(Constants.NGA_ZIP_FILE_PATH):
            print(Constants.NGA_ZIP_FILE_PATH)
            if os.path.exists(Const.NGA_FOLDER_RENAME_TO):
                shutil.rmtree(Const.NGA_FOLDER_RENAME_TO)
            self.extract_zip(Constants.NGA_ZIP_FILE_PATH, Const.NGA_CSV_DIR)
            # os.rename("downloads/opendata-main.zip", "downloads/old/opendata-main.zip")
        remove_old_and_create_new_sqlite_db()

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
                    self.extract_zip_and_recreate_db()
        else:
            print("No file found. Downloading...")
            self.download_zip(
                Const.NGA_REMOTE_DATA_ZIP, Constants.DOWNLOAD_FOLDER
            )
            self.extract_zip_and_recreate_db()

    @staticmethod
    def drop_unwanted_columns(df):
        for col in df.columns:
            if col not in Const.COLUMNS_USED:
                df.drop(col, axis=1, inplace=True)
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

        res.insert(0, 'source', 'NGA')
        res.to_csv(csv1_file_name, index=False)
        if os.path.exists(csv2_file_name):
            os.remove(csv2_file_name)

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

    def extract_zip(self, zip_name, extract_to):
        with ZipFile(zip_name, "r") as zip_f:
            zip_f.printdir()
            print("Extract start...")

            for file in zip_f.namelist():
                if file.startswith(Const.NGA_DOWNLOAD_STARTS_WITH):

                    end_part = file.split("data/")
                    end_part = end_part[len(end_part) - 1]
                    # print(end_part)
                    if end_part in Const.FILES_USED:
                        zip_f.extract(file, extract_to)

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
