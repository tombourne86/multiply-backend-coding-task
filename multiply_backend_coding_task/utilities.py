import re


def convert_camel_to_snake(name):
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


def format_snake_case(data):
    snake_data = {}
    for key in data:
        snake_data[convert_camel_to_snake(key)] = data[key]
    return snake_data


def email_is_valid(email_string):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    # regex taken from https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    return re.fullmatch(regex, email_string)


def find_next_available_id(store):
    if len(store) == 0:
        return "1"
    else:
        ids = [int(key) for key in store.keys()]
        new_id = max(ids) + 1
        return str(new_id)
