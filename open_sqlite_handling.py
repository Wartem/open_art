import sqlite3
import pandas as pd
from a_constants import *


def sqlite_creation_fill(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    create_table = '''CREATE TABLE IF NOT EXISTS objects(
            source TEXT NOT NULL,
            objectid TEXT NOT NULL, \
            title TEXT NOT NULL, \
            attribution TEXT, \
            beginyear INTEGER, \
            endyear INTEGER, \
            displaydate INTEGER, \
            classification TEXT NOT NULL, \
            medium TEXT,
            width INTEGER NOT NULL, \
            height INTEGER NOT NULL, \
            iiifurl TEXT NOT NULL PRIMARY KEY)
            '''

    cursor.execute(create_table)
    conn.commit()

    df = pd.read_csv(Constants.NGA_CSV_CONTAINER + "\\objects.csv",
                     on_bad_lines='skip', index_col=False, dtype='unicode')
    df.to_sql('objects', conn, if_exists='append', index=False, chunksize=1000)

    conn.close()


def query_builder():
    pass


def iter_containing_none(iter):
    for it in iter:
        if it is None:
            return True
    return False


def sql_injection(query: str, fetch_all=True, db_file=Constants.SQLite_OPEN_ART_DB_FILE_NAME) -> list:
    if not os.path.exists(db_file):
        print("SQLite db does not exists. Create one first.")
    else:

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        if query.startswith("SELECT"):
            cursor.execute(query)

            if fetch_all:
                rows = cursor.fetchall()
                return rows
            else:
                rows = cursor.fetchall()  # cursor.fetchone()[0]
                return [row[0] for row in rows]

        else:
            print("Only SELECT is allowed")
    return []


def sql_column_freq(col):
    return f"SELECT {col}, COUNT({col}) \
 AS count FROM objects GROUP BY {col} ORDER BY count DESC;"


def sql_column_all(col):
    return f"SELECT {col} FROM objects ORDER BY {col} ASC;"


def column_all(column_name):
    name_list = sql_injection(sql_column_all(column_name), False)
    res = filter(None, sorted(list(set(map(str, name_list)))))
    [print(r) for r in res]
    return name_list


def column_by_frequency(column_name):
    name_list = sql_injection(sql_column_freq(column_name), True)
    print(f"{column_name.capitalize()} in database, sorted by occurrence.")
    print(*(f"{name[0]} ({name[1]} occurrences)," for name in name_list), "\n" * 2)
    return name_list


def sql_injection_menu():
    while True:
        print("1. Type a sql injection")
        print("")
        print("2. Print frequency of all artists")
        print("3. Print frequency of all display dates")
        print("4. Print frequency of all begin years")
        print("5. Print frequency of all end years")
        print("6. Print frequency of all mediums")
        print("7. Print frequency of all classifications")
        print("")
        print("8. Print all artists")
        print("9. Print all display dates")
        print("10. Print all begin years")
        print("11. Print all end years")
        print("12. Print all mediums")
        print("13. Print all classifications")
        print("")
        print("14. Back to main menu.")
        num = input("Choose a number\n")

        match num:
            case "1":
                res = sql_injection(input("Type your SQL query\n"), True)
            case "2":
                artist = column_by_frequency("attribution")
            case "3":
                display_dates = column_by_frequency("displaydate")
            case "4":
                begin_year = column_by_frequency("beginyear")
            case "5":
                end_year = column_by_frequency("endyear")
            case "6":
                medium = column_by_frequency("medium")
            case "7":
                classification = column_by_frequency("classification")

            case "8":
                artist = column_all("attribution")
            case "9":
                display_dates = column_all("displaydate")
            case "10":
                begin_year = column_all("beginyear")
            case "11":
                end_year = column_all("endyear")
            case "12":
                medium = column_all("medium")
            case "13":
                classification = column_all("classification")
            case "14":
                break


'''
    query = "SELECT * FROM paintings_info WHERE " + columnname + " like '%" + rowValue + "%'";

    query = "SELECT * FROM paintings_info WHERE " + columnname + " like '" + rowValue + "%'";

    query = "SELECT * FROM paintings_info WHERE " + columnname + " = '" + rowValue + "'";
    

'''


def remove_old_and_create_new_sqlite_db():
    if os.path.exists(Constants.SQLite_OPEN_ART_DB_FILE_NAME):
        os.remove(Constants.SQLite_OPEN_ART_DB_FILE_NAME)
    sqlite_creation_fill(Constants.SQLite_OPEN_ART_DB_FILE_NAME)


def _sqlin(query):
    return ''.join(sql_injection(query))

def _gradion():
    import gradio as gr
    # 2. Create a Gradio interface with prefered input and output widgets
    app = gr.Interface(_sqlin, inputs=["text"], outputs=["text"])
    # 3. Launch the app. Bingo!
    app.launch()


if __name__ == '__main__':
    print("Not standalone")
    # name_list_test = sql_injection(
    # "SELECT attribution, COUNT(attribution) AS count FROM objects GROUP BY attribution ORDER BY count DESC")
    # print("Names of artists in database, sorted by number of artworks.")
    # sql_injection_menu()