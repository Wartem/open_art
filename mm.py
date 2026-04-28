import os
import time

import pandas as pd
import requests
import wget

from decorators import logger_exception_only
from open_source import Source

_MET_CSV_URL = "https://github.com/metmuseum/openaccess/raw/master/MetObjects.csv"
_MET_API_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/{}"


class MM(Source):

    def __init__(self):
        self.source_org_file_name = "MetObjects.csv"
        self.res_csv_file_name = "mm_paintings.csv"

    @logger_exception_only
    def download_open_data(self):
        if os.path.exists(self.source_org_file_name):
            print(f"{self.source_org_file_name} already exists, skipping download.")
            return
        print(f"Downloading {self.source_org_file_name} from Met Museum open access...")
        wget.download(_MET_CSV_URL, self.source_org_file_name)
        print()

    @logger_exception_only
    def unpack_and_create_csv(self):
        self.filter_update_fetch_fill_csv()

    def get_image_url_from_api(self, object_id: str) -> str:
        try:
            response = requests.get(
                _MET_API_URL.format(object_id), timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get("primaryImageSmall") or data.get("primaryImage") or ""
        except Exception:
            return ""

    @logger_exception_only
    def filter_update_fetch_fill_csv(self):
        if not os.path.exists(self.source_org_file_name):
            print(f"{self.source_org_file_name} not found. Run download first.")
            return

        if not os.path.exists(self.res_csv_file_name):
            with open(self.res_csv_file_name, "w"):
                pass

        df_source = pd.read_csv(
            self.source_org_file_name,
            on_bad_lines="skip",
            index_col=False,
            dtype="unicode",
        )

        df_filtered = df_source[
            (df_source["Classification"] == "Painting")
            & (df_source["Is Public Domain"] == "True")
        ].copy()

        df_existing = pd.DataFrame()
        if os.path.getsize(self.res_csv_file_name):
            df_existing = pd.read_csv(
                self.res_csv_file_name,
                on_bad_lines="skip",
                index_col=False,
                dtype="unicode",
            )

        existing_ids = set(df_existing["objectid"].values) if not df_existing.empty else set()
        total = len(df_filtered)

        for count, (_, row) in enumerate(df_filtered.iterrows(), 1):
            object_id = str(row["Object ID"]).strip()

            if object_id in existing_ids:
                print(f"Skipping {object_id} (already in csv) [{count}/{total}]")
                continue

            print(f"Fetching {object_id} [{count}/{total}]...")
            img_url = self.get_image_url_from_api(object_id)

            if not img_url:
                print(f"  No image found for {object_id}, skipping.")
                continue

            obj = {
                "source": "MM",
                "objectid": object_id,
                "title": str(row["Title"]).strip(),
                "attribution": str(row["Artist Display Name"]).strip(),
                "beginyear": str(row["Object Begin Date"]).strip(),
                "endyear": str(row["Object End Date"]).strip(),
                "displaydate": str(row["Object Date"]).strip(),
                "classification": str(row["Classification"]).strip(),
                "medium": str(row["Medium"]).strip(),
                "width": "",
                "height": "",
                "imgurl_thumb": img_url,
                "imgurl_downsized": img_url,
                "imgurl_full": img_url,
            }

            df_row = pd.DataFrame([obj])
            write_header = df_existing.empty and count == 1
            df_row.to_csv(
                self.res_csv_file_name,
                mode="w" if write_header else "a",
                header=write_header,
                index=False,
                encoding="utf-8",
            )
            existing_ids.add(object_id)
            time.sleep(0.1)


if __name__ == "__main__":
    mm = MM()
    mm.download_open_data()
    mm.filter_update_fetch_fill_csv()
