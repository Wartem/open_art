from csv_handling import \
    init, \
    choose_art_data, \
    print_file_names, \
    investigate


def csv_menu_loop():
    print("\n")
    init()
    art_dir_in_use = choose_art_data()
    
    if art_dir_in_use is None:
        print("No valid directory selected. Returning to main menu.")
        return
    
    while art_dir_in_use:
        print("")
        print("Welcome to Art Data Info")
        print(
            "Directory in use:", art_dir_in_use
        ) if art_dir_in_use else "No directory found!"
        # pprint("Diretory in use: " + art_dir_in_use) if art_dir_in_use else "No directory found!"
        print("Type feature corresponding number:")
        print("1. Print all available files.")
        print("2. Type filename to investigate.")
        print("3. Main menu.")

        match input("Type a input number from above\n"):
            case "1":
                print_file_names()
                input("\nPress Enter to continue...")
            case "2":
                investigate()
            case "3":
                break

if __name__ == '__main__':
    print("Not standalone")
