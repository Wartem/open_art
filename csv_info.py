import datetime
import time
import os
import platform


def get_month_name_from_int(months, num):
    for key, value in months.items():
        if num == value:
            return key
    return num


def creation_date(path_to_file) -> tuple:
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == "Windows":
        return os.path.getmtime(path_to_file), os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime, None
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime, None


def get_file_creation_date(filename) -> tuple:
    times = creation_date(filename)
    
    creation_time = time.ctime(times[0])
    creation_time = datetime.datetime.strptime(creation_time, "%a %b %d %H:%M:%S %Y")
    creation_time = datetime.datetime(creation_time.year, creation_time.month, creation_time.day)
    
    altered_time = time.ctime(times[1]) if times[1] else creation_time
    if altered_time:
        altered_time = datetime.datetime.strptime(altered_time, "%a %b %d %H:%M:%S %Y")
        altered_time = datetime.datetime(altered_time.year, altered_time.month, altered_time.day)
    
    return creation_time, altered_time