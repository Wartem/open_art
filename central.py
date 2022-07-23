

from this import d
import pandas as pd
from a_constants import Constants
import re

#nga = NGA()
#mm = MM()

#nga.download_open_data()

ints = ["beginyear", "endyear", "width", "height", "displaydate"]

res_csv_file_name = "res.csv"
nga_csv = Constants.NGA_CSV_CONTAINER + "\\" + "objects.csv"

def fill_empty_cells(df: pd.DataFrame) -> None:
 
    for col in df:
        if col in ints:
            df[col].fillna(0, inplace = True)
        else:
            df[col].fillna(f"Unknown {col}", inplace = True)

    return df
    
def fill_empty_cells2(df: pd.DataFrame, column_name: str) -> None:
 
    for ind in df.index:
        if pd.isnull(df.at[ind, column_name]):
                if column_name in ints:
                    df.at[ind, column_name] = 0
                else:
                    df.at[ind, column_name] = f"Unknown {column_name}"
                # print(df.at[ind, column_name])
                
    for ind in df.index:
        print(df.at[ind, "displaydate"])
    return df

def concat():
    
    mm = pd.read_csv("mm_paintings.csv", on_bad_lines='skip', \
                index_col=False, dtype='unicode')
    nga = pd.read_csv(nga_csv, on_bad_lines='skip', \
                index_col=False, dtype='unicode')
    
    # df3 = nga.append(mm, ignore_index=True)
    df3 = pd.concat([nga, mm], axis=0, ignore_index=True)
    
    
    # Remove invalid rows
    for ind in df3.index:
        #print("check", df3.index[ind])
        if not "http" in str(df3['imgurl_full'][ind]) or \
            not str(df3['objectid'][ind]):
            print(df3.index[ind])
            df3.drop(df3.index[ind], axis=0, inplace=True)
    
    df3 = fill_empty_cells(df3)
          
    df3.to_csv(res_csv_file_name, index=False, encoding='utf-8')
    
    
import sqlite3
import pandas as pd
from a_constants import *

def remove_old_and_create_new_sqlite_db():
    if os.path.exists(Constants.SQLite_OPEN_ART_DB_FILE_NAME):
        os.remove(Constants.SQLite_OPEN_ART_DB_FILE_NAME)
    create_common_db(Constants.SQLite_OPEN_ART_DB_FILE_NAME)
    
def create_common_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    create_table = ''' CREATE TABLE IF NOT EXISTS objects(
            source TEXT NOT NULL,
            objectid TEXT NOT NULL, \
            title TEXT NOT NULL, \
            attribution TEXT NOT NULL, \
            beginyear INTEGER NOT NULL, \
            endyear INTEGER NOT NULL, \
            displaydate INTEGER NOT NULL, \
            classification TEXT NOT NULL, \
            medium TEXT NOT NULL, \
            width INTEGER NOT NULL, \
            height INTEGER NOT NULL, \
            imgurl_thumb TEXT NOT NULL, \
            imgurl_downsized TEXT NOT NULL, \
            imgurl_full TEXT NOT NULL PRIMARY KEY); '''

    cursor.execute(create_table)
    conn.commit()

    df = pd.read_csv("res.csv",
                     on_bad_lines='skip', index_col=False, dtype='unicode')
    df.to_sql('objects', conn, if_exists='append', index=False, chunksize=1000)

    conn.close()

if __name__ == '__main__':
    concat()
    remove_old_and_create_new_sqlite_db()
