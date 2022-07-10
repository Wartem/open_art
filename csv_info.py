import datetime
import time
import os
import platform


def get_month_name_from_int(months, num):
    for key, value in months.items():
        if num == value:
            return key
    return num


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == "Windows":
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def get_file_creation_date(filename):
    timed = time.ctime(creation_date(filename))
    f_date = datetime.datetime.strptime(timed, "%a %b %d %H:%M:%S %Y")
    return datetime.datetime(f_date.year, f_date.month, f_date.day)