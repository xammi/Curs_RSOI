import datetime

DELIMITER = '.'


def smart_get(store: dict, delimited_name: str, default: str = None):
    for name in delimited_name.split(DELIMITER):
        store = store.get(name, default)
        if not isinstance(store, dict):
            return store
    return store


def convert_date(str_date, from_fmt, to_fmt):
    date_obj = datetime.datetime.strptime(str_date, from_fmt)
    return date_obj.strftime(to_fmt)
