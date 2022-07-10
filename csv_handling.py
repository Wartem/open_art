import os
import glob

from csv_art import Art_csv
from a_constants import Constants as Const

csv_directory_in_use = ""
root_dir_folders = []
csv_file_names = []


def init():
    global root_dir_folders
    root_dir_folders = os.listdir(Const.NGA_CSV_DIR)
    print_folder_names()
    # csv_files = glob.glob(os.path.join(path, "*.csv"))


def print_folder_names():
    print("Folders:")
    for folder_name in root_dir_folders:
        print("--> ", folder_name)


def print_file_names():
    print("File names:")
    for file_name in csv_file_names:
        print(file_name)


def set_csv_folder(user_dir):
    # path = os.getcwd()
    global csv_directory_in_use
    csv_directory_in_use = Const.NGA_CSV_DIR + user_dir + "\\data\\"
    global csv_file_names
    csv_file_names = glob.glob(os.path.join(csv_directory_in_use, "*.csv"))


def choose_art_data():
    if root_dir_folders:
        user_dir = input("Choose an art data directory name from the list above.\n")
        if user_dir in root_dir_folders:
            set_csv_folder(user_dir)
            return csv_directory_in_use

    print("Directory not found.")
    return None


def type_file_name():
    user_input = input("Type the name of the file to use\n")
    if csv_directory_in_use not in user_input:
        user_input = csv_directory_in_use + user_input
    if not user_input.endswith(".csv"):
        user_input += ".csv"
    for file in csv_file_names:
        if user_input in file:
            return user_input

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
            print("1. Print all rows in columns in: " + file_to_use)
            print("2. Back to main menu.")
            d = input("Choose a number\n")
            if d == "1":
                print(art_csv.get_column_data(input("Type column name\n")))
            if d == "2":
                break

if __name__ == '__main__':
    print("Not standalone")