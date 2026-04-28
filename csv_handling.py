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
    art_dirs = [d for d in Constants.NGA_open_data_art.iterdir() if d.is_dir()]

    if not art_dirs:
        print("No art data directories found.")
        return None

    print(f"\nAvailable directories ({len(art_dirs)}):")
    for i, art_dir in enumerate(art_dirs, 1):
        print(f"  {i:>2}. {art_dir.name}")
    print()

    while True:
        raw = input("Enter directory name or number: ").strip()
        if not raw:
            continue
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(art_dirs):
                set_csv_folder(art_dirs[idx].name)
                return csv_directory_in_use
            print(f"  Number out of range (1-{len(art_dirs)}). Try again.")
            continue
        if Path(Constants.NGA_open_data_art / raw).is_dir():
            set_csv_folder(raw)
            return csv_directory_in_use
        print(f"  '{raw}' not found. Try again.")


def type_file_name():
    if not csv_file_names:
        print("No CSV files found in the selected directory.")
        return ""
    print(f"\nAvailable files ({len(csv_file_names)}):")
    for i, f in enumerate(csv_file_names, 1):
        print(f"  {i:>2}. {f.name}")
    print()
    while True:
        raw = input("Enter file name or number: ").strip()
        if not raw:
            return ""
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(csv_file_names):
                return str(csv_file_names[idx])
            print(f"  Number out of range (1-{len(csv_file_names)}). Try again.")
            continue
        file_path = csv_directory_in_use / raw
        if not file_path.suffix:
            file_path = file_path.with_suffix(".csv")
        for file in csv_file_names:
            if file_path.name in file.name:
                return str(file)
        print(f"  File '{raw}' not found. Try again.")


def _print_columns(art_csv):
    cols = list(art_csv.data.columns)
    print(f"\nAvailable columns ({len(cols)}):")
    for i, col in enumerate(cols, 1):
        print(f"  {i:>2}. {col}")
    print()
    return cols


def _pick_column(art_csv):
    cols = _print_columns(art_csv)
    while True:
        raw = input("Enter column name or number (blank to cancel): ").strip()
        if not raw:
            return None
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(cols):
                return cols[idx]
            print(f"  Number out of range (1-{len(cols)}). Try again.")
            continue
        resolved = art_csv.resolve_column(raw)
        if resolved:
            return resolved
        print(f"  Column '{raw}' not found. Try again.")


def investigate():
    file_to_use = type_file_name()
    if not file_to_use:
        print("File Not Found.")
        return

    art_csv = Art_csv(file_to_use)
    art_csv.print_report()

    while True:
        print(f"\nFile: {file_to_use}")
        print("1. Print column data")
        print("2. Back to file menu")
        d = input("Choose a number: ").strip()
        if d == "1":
            col = _pick_column(art_csv)
            if col is None:
                continue
            data = art_csv.get_column_data(col)
            if data is None:
                print("Column not found.")
            else:
                print(data.to_string())
            input("\nPress Enter to continue...")
        elif d == "2":
            break


if __name__ == "__main__":
    print("Not standalone")
