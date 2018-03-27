from functools import wraps

from flask import json


def add_tag(tag):
    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f'<{tag}>{f(*args, **kwargs)}</{tag}>'
        return wrapper
    return inner


@add_tag('h1')
def write_something():
    return 'something'


result = write_something()
assert result == '<h1>something</h1>'


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


@validate_json('first_name', 'last_name')
def process_json(json_data):
    return len(json_data)


result = process_json('{"first_name": "James", "last_name": "Bond"}')
assert result == 44
