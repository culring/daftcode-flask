from functools import wraps
from flask import json
import logging


def add_tag(tag):
    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f'<{tag}>{f(*args, **kwargs)}</{tag}>'
        return wrapper
    return inner


# @add_tag('h1')
# def write_something():
#     return 'something'


def validate_json(*keys):
    def inner(f):
        @wraps(f)
        def wrapper(json_data):
            js = json.loads(json_data)
            if len(keys) != len(js):
                raise ValueError
            for key in keys:
                if key not in js:
                    raise ValueError
            return f(json_data)
        return wrapper
    return inner


# @validate_json('first_name', 'last_name')
# def process_json(json_data):
#     return len(json_data)


def log_this(logger, level=logging.INFO, format=''):
    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            logging.basicConfig(level=level)
            arguments = [str(x) for x in args] + [str(k) + '=' + str(v) for k, v in kwargs.items()]
            rv = f(*args, **kwargs)
            logger.info(format, f.__name__, tuple(arguments), rv)
        return wrapper
    return inner


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# @log_this(logger, level=logging.WARNING, format='%s: %s -> %s')
# def my_func(a, b, c=None, d=False):
#     return 'Wow!'
