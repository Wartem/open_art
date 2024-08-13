import os
from pathlib import Path
from typing import Dict, List

class Constants:
    months_abbreviated: Dict[str, int] = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
    }

    APP_NAME: str = "OpenArt"

    PARENT_PATH: Path = Path(__file__).resolve().parent.parent
    DOWNLOAD_FOLDER: Path = PARENT_PATH / APP_NAME.lower() / "downloads"
    SQLite_OPEN_ART_DB_FILE_NAME: Path = PARENT_PATH / APP_NAME.lower() / "open_data_art" / "open_art.db"

    # NGA
    COLUMNS_USED: List[str] = [
        "objectid", "title", "attribution", "beginyear", "endyear", "displaydate", 
        "classification", "medium", "width", "height", "iiifurl"
    ]

    OBJECTS_AND_PUBLISHED_IMAGES: List[str] = [
        "objectid", "accessioned", "accessionnum", "locationid", "title", "displaydate",
        "beginyear", "endyear", "visualbrowsertimespan", "medium", "dimensions", 
        "inscription", "markings", "attributioninverted", "attribution", "provenancetext", 
        "creditline", "classification", "subclassification", "visualbrowserclassification", 
        "parentid", "isvirtual", "departmentabbr", "portfolio", "series", "volume", 
        "watermarks", "lastdetectedmodification", "customprinturl", "uuid", "iiifurl", 
        "iiifthumburl", "viewtype", "sequence", "width", "height", "maxpixels", "created",
        "modified", "depictstmsobjectid", "assistivetext"
    ]

    FILES_USED: List[str] = ["objects.csv", "published_images.csv"]

    NGA_open_data_art: Path = PARENT_PATH / APP_NAME.lower() / "open_data_art"
    NGA_FOLDER_RENAME_TO: Path = NGA_open_data_art / "nga"
    NGA_CSV_CONTAINER: Path = NGA_FOLDER_RENAME_TO / "opendata-main" / "data"
    NGA_DOWNLOAD_STARTS_WITH: str = "opendata-main/data/"
    
    NGA_ZIP_FILE_NAME: str = "opendata-main.zip"
    NGA_ZIP_FILE_PATH: Path = DOWNLOAD_FOLDER / NGA_ZIP_FILE_NAME

    NGA_REMOTE_DATA_ZIP: str = "https://github.com/NationalGalleryOfArt/opendata/archive/refs/heads/main.zip"

    @classmethod
    def print_constants(cls) -> None:
        for attr, value in cls.__dict__.items():
            if not attr.startswith("__") and not callable(value):
                print(f"{attr}: {value}")

if __name__ == "__main__":
    Constants.print_constants()