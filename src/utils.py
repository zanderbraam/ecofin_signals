from pathlib import Path
from dateutil.parser import parse


def get_project_root():
    """
    Return the project root path

    :return: string path
    """
    return Path(__file__).parent.parent


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


