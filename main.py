import os
from csv_menu import csv_menu_loop
from nga import NGA
from open_sqlite_handling import sql_injection_menu
from a_constants import *


def init():
    if not os.path.exists("open_data_art"):
        os.makedirs("open_data_art")
    if not os.path.exists("downloads"):
        os.makedirs("downloads")


def menu():
    is_windows = "Windows" in os.getenv('OS')
    user_name = os.getenv('HOMEPATH').rsplit("\\")
    user_name = user_name[len(user_name) - 1] if is_windows else \
        "<Not Windows User (that's fine!)>"

    while True:
        print(
            "",
            f"Welcome {user_name}, {os.getenv('USERDOMAIN')} to {Constants.APP_NAME}",
            "Choose an option/number from the list below",
            sep=f"\n[{Constants.APP_NAME}]: ",
            end="\n",
        )
        # print([print(x, y) for x,y in os.environ.items()])
        """ for key, value in os.environ.items():
            print (key, value)
            print() """
        print("1. Download data if needed from art source/museum")
        print("2. Extract existing zip file and replace database")
        print("3. SQLite injection and db statistics")
        print("4. Open file information")
        print("5. System exit")
        menu_val = input("Enter the corresponding menu number: ")

        nga = NGA()

        match menu_val:
            case "0":
                pass
                # sqlite_ex.start_app(debug=True)
            case "1":
                nga.download_zip_if_needed()
            case "2":
                nga.unpack_and_create_csv()
            case "3":
                sql_injection_menu()
            case "4":
                # menu_csv = Menu_csv(OPEN_DATA_CSV_FILES_LOCATION)
                csv_menu_loop()
            case "5":
                print("System exits")
                break


def main():
    init()
    #print_constants()
    menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exit by user")