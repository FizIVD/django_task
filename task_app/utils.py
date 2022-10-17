from typing import Any
import json


def validate(**fields):
    none_fields = [i for i in fields if fields[i] is None]
    if none_fields:
        raise Exception(f'Fields: {", ".join(none_fields)} is required')


def parse_body(body: Any):
    """Return parsed into a dict request json"""
    try:
        body = json.loads(body.decode('utf-8'))
    except json.JSONDecodeError:
        body = {}
    return body


def dict_fetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def fields_to_update(model):
    """Return formated for query string with fields to update"""
    lst = [f"{i} = '{model.__dict__[i]}'"
           for i in model.__dict__
           if i != 'id' and model.__dict__[i] is not None]
    return ", ".join(lst)


def fields_to_save(model):
    """Return formated for query string with fields to save"""
    lst = [i
           for i in model.__dict__
           if model.__dict__[i] is not None]
    return ", ".join(lst)


def values_to_save(model):
    """Return formated for query string with fields values to save"""
    lst = [f"'{str(model.__dict__[i])}'"
           for i in model.__dict__
           if model.__dict__[i] is not None]
    return ", ".join(lst)
