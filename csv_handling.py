import glob
from pathlib import Path

from a_constants import Constants
from csv_art import Art_csv

csv_directory_in_use = Path()
root_dir_folders = []
csv_file_names = []


def init():
    global root_dir_folders
    root_dir_folders = [f for f in Constants.NGA_open_data_art.iterdir() if f.is_dir()]
    # print_folder_names()


def print_folder_names():
    print("Folders:")
    for folder_name in root_dir_folders:
        print(f"--> {folder_name.name}")


def print_file_names():
    print("File names:")
    for file_name in csv_file_names:
        print(file_name.name)


def set_csv_folder(user_dir):
    global csv_directory_in_use
    csv_directory_in_use = (
        Constants.NGA_open_data_art / user_dir / "opendata-main" / "data"
    )
    global csv_file_names
    csv_file_names = list(csv_directory_in_use.glob("*.csv"))


def choose_art_data():
    print("\nFolders:")
    art_dirs = [d for d in Constants.NGA_open_data_art.iterdir() if d.is_dir()]
    for art_dir in art_dirs:
        print(f"--> {art_dir.name}")

    if not art_dirs:
        print("No art data directories found.")
        return None

    print("Choose an art data directory name from the list above.")
    while True:
        user_dir = input()
        if Path(Constants.NGA_open_data_art / user_dir).is_dir():
            set_csv_folder(user_dir)
            return csv_directory_in_use
        else:
            print("Invalid directory. Please choose from the list above.")


def type_file_name():
    user_input = input("Type the name of the file to use\n")
    file_path = csv_directory_in_use / user_input
    if not file_path.suffix:
        file_path = file_path.with_suffix(".csv")

    for file in csv_file_names:
        if file_path.name in file.name:
            return str(file)

    return ""


def investigate():
    file_to_use = type_file_name()
    while True:
        if not file_to_use:
            print("File Not Found.")
            break
        else:
            art_csv = Art_csv(file_to_use)
            art_csv.print_report()
            print(f"1. Print all rows in columns in: {file_to_use}")
            print("2. Back to main menu.")
            d = input("Choose a number\n")
            if d == "1":
                print(art_csv.get_column_data(input("Type column name\n")))
            if d == "2":
                break


if __name__ == "__main__":
    print("Not standalone")
