# Standard library imports
import os
import sys
import glob
import shutil
import datetime
from zipfile import ZipFile

# Third-party library imports
import requests
import wget
import pandas as pd
from bs4 import BeautifulSoup

# Local imports
from a_constants import Constants
from csv_info import get_file_creation_date, get_month_name_from_int
from open_source import Source

from pathlib import Path
from datetime import datetime
from dateutil import parser


class NGA(Source):

    def __init__(self):
        self.objects = []

    def download_open_data(self):
        self.download_zip_if_needed()

    def unpack_and_create_csv(self):
        self.extract_zip_and_fix()


    @staticmethod
    def _get_nga_latest_remote_git_update_date():
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
    
    
    @staticmethod
    def get_nga_latest_remote_git_update_date():
        url = "https://api.github.com/repos/NationalGalleryOfArt/opendata/commits"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes

            commits = response.json()
            if commits:
                latest_commit = commits[0]
                commit_date = parser.parse(latest_commit['commit']['committer']['date'])
                return commit_date.replace(tzinfo=None)  # Remove timezone info for consistency
            else:
                print("No commits found")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching commit data: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"Error parsing commit data: {e}")
            return None


    def is_nga_file_update_needed(self):
        git_date = self.get_nga_latest_remote_git_update_date()
        local_file_path = Constants.NGA_ZIP_FILE_PATH
        
        if local_file_path.exists():
            creation_date, altered_date = get_file_creation_date(str(local_file_path))

            if git_date > creation_date:
                print(f"A seemingly newer version is available for {Constants.NGA_REMOTE_DATA_ZIP}")
            else:
                print(f"Your file is up to date. No need to download again from\n{Constants.NGA_REMOTE_DATA_ZIP}")

            print(
                f"File on server was uploaded: {git_date.year} "
                f"{self.get_month_name_from_int(Constants.months_abbreviated, git_date.month)} {git_date.day}"
            )
            print(
                f"Your downloaded local file ({local_file_path}) is from: {creation_date.year} "
                f"{self.get_month_name_from_int(Constants.months_abbreviated, creation_date.month)} {creation_date.day}"
            )

            if creation_date < altered_date:
                print(
                    f"Your downloaded local file ({local_file_path}) was last changed: {altered_date.year} "
                    f"{self.get_month_name_from_int(Constants.months_abbreviated, altered_date.month)} {altered_date.day}"
                )

            return git_date > creation_date
        else:
            print(f"Local file not found. Downloading from {Constants.NGA_REMOTE_DATA_ZIP}")
            return True

    @staticmethod
    def get_month_name_from_int(months_dict, month_number):
        return list(months_dict.keys())[list(months_dict.values()).index(month_number)]


    def download_zip_if_needed(self):
        if Constants.NGA_ZIP_FILE_PATH.exists():
            self.is_nga_file_update_needed()
            if input("Remove and replace the existing file? yes/no ").lower() == "yes":
                if Constants.NGA_ZIP_FILE_PATH.exists():
                    Constants.NGA_ZIP_FILE_PATH.unlink()
                    print("Old file removed.")

                self.download_zip(Constants.NGA_REMOTE_DATA_ZIP, str(Constants.DOWNLOAD_FOLDER))
                if input(
                    f"Extract the downloaded {Constants.NGA_ZIP_FILE_NAME} "
                    "and create/replace the database? \nyes/no "
                ).lower() == "yes":
                    self.extract_zip_and_fix()
        else:
            print("No file found. Downloading...")
            self.download_zip(Constants.NGA_REMOTE_DATA_ZIP, str(Constants.DOWNLOAD_FOLDER))
            self.extract_zip_and_fix()

    def download_zip_if_needed(self):
        if Constants.NGA_ZIP_FILE_PATH.exists():
            self.is_nga_file_update_needed()
            if input("Remove and replace the existing file? yes/no ").lower() == "yes":
                if Constants.NGA_ZIP_FILE_PATH.exists():
                    Constants.NGA_ZIP_FILE_PATH.unlink()
                    print("Old file removed.")

                self.download_zip(Constants.NGA_REMOTE_DATA_ZIP, str(Constants.DOWNLOAD_FOLDER))
                if input(
                    f"Extract the downloaded {Constants.NGA_ZIP_FILE_NAME} "
                    "and create/replace the database? \nyes/no "
                ).lower() == "yes":
                    self.extract_zip_and_fix()
        else:
            print("No file found. Downloading...")
            self.download_zip(Constants.NGA_REMOTE_DATA_ZIP, str(Constants.DOWNLOAD_FOLDER))
            self.extract_zip_and_fix()


    @staticmethod
    def drop_unwanted_columns(df: pd.DataFrame):
        for col in df.columns:
            if col not in Constants.COLUMNS_USED:
                df.drop(col, axis=1, inplace=True)
        return df


    def fix_image_properties(self, df: pd.DataFrame):

        for index, row in df.iterrows():
            # print(row["width"][index])
            width = int(df["width"][index])
            height = int(df["height"][index])
            iiifurl = str(df["iiifurl"][index])

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
                imgurl_downsized = iiifurl + \
                    f"/full/!{str(width)},{str(height)}/0/default.jpg"

            imgurl_thumb = iiifurl + "/full/!200,200/0/default.jpg"

            df.at[index, "source"] = "NGA"
            df.at[index, "imgurl_thumb"] = imgurl_thumb
            df.at[index, "imgurl_downsized"] = imgurl_downsized
            df.at[index, "imgurl_full"] = imgurl_full

        return df


    def merge(self, csv1_file_name, csv2_file_name):
        # reading two csv files
        df1 = pd.read_csv(csv1_file_name, on_bad_lines='skip',
                          index_col=False, dtype='unicode')
        df2 = pd.read_csv(csv2_file_name, on_bad_lines='skip',
                          index_col=False, dtype='unicode')

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
        art_folder_path = Path(art_folder)
        csv_file_names = list(art_folder_path.glob("*.csv"))

        # Prepare merge objects.csv with published_images.csv
        for file in csv_file_names:
            if file.name == "published_images.csv":
                df = pd.read_csv(file, on_bad_lines='skip', index_col=False, dtype='unicode')
                df.rename(columns={'depictstmsobjectid': 'objectid'}, inplace=True)
                df.to_csv(file)

        objects_csv = art_folder_path / "objects.csv"
        published_images_csv = art_folder_path / "published_images.csv"

        if objects_csv.exists() and published_images_csv.exists():
            print(f"Merging {objects_csv} with {published_images_csv}")
            # Merging
            self.merge(str(objects_csv), str(published_images_csv))
        else:
            print("One or both of the required CSV files are missing.")

    def merge(self, objects_csv_path, published_images_csv_path):
        # Implement your merge logic here
        pass


    def extract_zip_and_fix(self):
        if Constants.NGA_ZIP_FILE_PATH.exists():
            print(f"Extracting from: {Constants.NGA_ZIP_FILE_PATH}")
            
            # Create the directory structure if it doesn't exist
            Constants.NGA_CSV_CONTAINER.mkdir(parents=True, exist_ok=True)
            
            with ZipFile(Constants.NGA_ZIP_FILE_PATH, "r") as zip_f:
                zip_f.printdir()
                print("Extract start...")
                for file in zip_f.namelist():
                    if file.startswith("opendata-main/data/"):
                        end_part = file.split("data/")[-1]
                        if end_part in Constants.FILES_USED:
                            print(f"Extracting: {file}")
                            zip_f.extract(file, Constants.NGA_FOLDER_RENAME_TO)
                
                print(f"Extraction complete. Files should be in: {Constants.NGA_CSV_CONTAINER}")
                print(f"Cleaning up files in: {Constants.NGA_CSV_CONTAINER}")
                self.fix_nga_csv_in_folder(Constants.NGA_CSV_CONTAINER)
        else:
            print(f"Zip file not found: {Constants.NGA_ZIP_FILE_PATH}")


    def _extract_zip_and_fix(self):
        if os.path.exists(Constants.NGA_ZIP_FILE_PATH):
            print(Constants.NGA_ZIP_FILE_PATH)
            if os.path.exists(Constants.NGA_FOLDER_RENAME_TO):
                shutil.rmtree(Constants.NGA_FOLDER_RENAME_TO)
            
            with ZipFile(Constants.NGA_ZIP_FILE_PATH, "r") as zip_f:
                zip_f.printdir()
                print("Extract start...")
                for file in zip_f.namelist():
                    # Convert WindowsPath to string
                    nga_download_starts_with = str(Constants.NGA_DOWNLOAD_STARTS_WITH)
                    if file.startswith(nga_download_starts_with):
                        end_part = file.split("data/")[-1]
                        if end_part in Constants.FILES_USED:
                            zip_f.extract(file, Constants.NGA_FOLDER_RENAME_TO)
                
                if zip_f.namelist():
                    # Construct the full path for the folder to be renamed
                    old_folder_path = os.path.join(Constants.NGA_open_data_art, Constants.NGA_FOLDER_TO_RENAME)
                    # Rename the folder
                    if os.path.exists(old_folder_path):
                        os.rename(old_folder_path, Constants.NGA_FOLDER_RENAME_TO)
                    
                    print("Now cleaning up the files in", Constants.NGA_CSV_CONTAINER)
                    self.fix_nga_csv_in_folder(Constants.NGA_CSV_CONTAINER)
                    print("Extract complete!")
                else:
                    print("Extract failed.")


    def download_zip(self, data_url, download_folder):
        def bar_progress(current, total, width=80):
            progress_message = f"Downloading: {current / total * 100:.2f}% [{current} / {total}] bytes"
            sys.stdout.write("\r" + progress_message)
            sys.stdout.flush()

        # Convert Path object to string
        download_folder_str = str(download_folder)

        try:
            file = wget.download(data_url, download_folder_str, bar=bar_progress)
            print("\nDownload completed successfully.")
            return file
        except Exception as e:
            print(f"\nAn error occurred during download: {e}")
            return None


    def bar_progress(current, total, width=80):
        progress_message = "Downloading: %d%% [%d / %d] bytes" % (
            current / total * 100, current, total)
        # Don't use print() as it will print in new line every time.
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()


if __name__ == "__main__":
    print("No main. Call functions instead.")