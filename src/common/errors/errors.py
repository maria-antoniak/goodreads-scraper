import functools


def return_none_for_attribute_error(func):
    @functools.wraps(func)
    def wrapper(*args):
        """
        e.g Trying to get href from a non existent bs4 object.
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
        e.g Trying to get href from a non existent bs4 object.
        """
        try:
            return func(args[0])
        except TypeError:
            return None

    return wrapper


def return_none_for_index_error(func):
    @functools.wraps(func)
    def wrapper(*args):
        """
        e.g Trying to slice an empty list.
        """
        try:
            return func(args[0])
        except IndexError:
            return None

    return wrapper


def return_none_for_assertion_error(func):
    @functools.wraps(func)
    def wrapper(*args):
        try:
            return func(args[0])
        except AssertionError:
            return None

    return wrapper
