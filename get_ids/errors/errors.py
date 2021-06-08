import functools


def return_none_for_attribute_error(func):
    @functools.wraps(func)
    def wrapper(*args):
        """
        e.g Trying to convert bs4 object into text when it is not present.
        """
        try:
            return func(args[0])
        except AttributeError:
            return None

    return wrapper


def return_none_for_type_error(func):
    @functools.wraps(func)
    def wrapper(*args):
        """
        e.g Trying to to get href from a non existent bs4 object.
        """
        try:
            return func(args[0])
        except TypeError:
            return None

    return wrapper
