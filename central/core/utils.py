DELIMITER = '.'


def smart_get(store: dict, delimited_name: str, default: str = None):
    for name in delimited_name.split(DELIMITER):
        store = store.get(name, default)
        if not isinstance(store, dict):
            return store
    return store
