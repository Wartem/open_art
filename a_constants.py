import os


# TODO: upgrade to pathlib path
# TODO: Environment Variables:
#       making-use-of-environment-variables-in-python

# __all__ = ["APP_NAME", OPEN_DATA_NGA_FILE]

def print_constants():
    print("APP_NAME", Constants.APP_NAME)
    print("PARENT_PATH", Constants.PARENT_PATH)
    print("DOWNLOAD_FOLDER", Constants.DOWNLOAD_FOLDER)

    # NGA
    print("NGA_CSV_DIR", Constants.NGA_open_data_art)

    print("NGA_ART_DATA_ZIP", Constants.NGA_REMOTE_DATA_ZIP)
    print("NGA_ZIP_FILE", Constants.NGA_ZIP_FILE_NAME)

    print("NGA_DOWNLOAD_STARTS_WITH", Constants.NGA_DOWNLOAD_STARTS_WITH)
    print("NGA_FOLDER_TO_RENAME", Constants.NGA_FOLDER_TO_RENAME)
    print("NGA_FOLDER_RENAME_TO", Constants.NGA_FOLDER_RENAME_TO)
    print("NGA_CSV_CONTAINER", Constants.NGA_CSV_CONTAINER)


class Constants:
    months_abbreviated = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }

    APP_NAME = "OpenArt"

    PARENT_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    DOWNLOAD_FOLDER = PARENT_PATH + "\\" + APP_NAME.lower() + "\\" + "downloads\\"
    SQLite_OPEN_ART_DB_FILE_NAME = PARENT_PATH + "\\" + APP_NAME.lower() + "\\" + "open_data_art\open_art.db"


    # NGA

    COLUMNS_USED = ["objectid", "title", "attribution", "beginyear", "endyear", "displaydate", "classification",
                    "medium",
                    "width", "height", "iiifurl"]

    OBJECTS_AND_PUBLISHED_IMAGES = ["objectid", "accessioned", "accessionnum", "locationid", "title", "displaydate",
                                    "beginyear", "endyear", "visualbrowsertimespan",
                                    "medium", "dimensions", "inscription", "markings", "attributioninverted",
                                    "attribution","provenancetext", "creditline", "classification",
                                    "subclassification", "visualbrowserclassification", "parentid", "isvirtual",
                                    "departmentabbr", "portfolio", "series", "volume", "watermarks",
                                    "lastdetectedmodification","customprinturl", "uuid", "iiifurl", "iiifthumburl",
                                    "viewtype", "sequence","width","height", "maxpixels", "created",
                                    "modified", "depictstmsobjectid", "assistivetext"]

    FILES_USED = ["objects.csv", "published_images.csv"]

    NGA_open_data_art = PARENT_PATH + "\\" + APP_NAME.lower() + "\\" + "open_data_art\\"

    NGA_REMOTE_DATA_ZIP = (
        "https://github.com/NationalGalleryOfArt/opendata/archive/refs/heads/main.zip"
    )
    NGA_ZIP_FILE_NAME = "opendata-main.zip"
    NGA_DOWNLOAD_STARTS_WITH = "opendata-main/data/"
    NGA_FOLDER_TO_RENAME = "opendata-main"
    NGA_FOLDER_RENAME_TO = NGA_open_data_art + "nga"
    NGA_CSV_CONTAINER  = NGA_FOLDER_RENAME_TO + "\\opendata-main\\data" # used to be only \\data
    NGA_ZIP_FILE_PATH = DOWNLOAD_FOLDER + NGA_ZIP_FILE_NAME


