from typing import Any
import json


def validate(**fields: dict) -> None:
    """Возвращает исключение, если отсутствуют значения в необходимых полях"""
    none_fields = [i for i in fields if fields[i] is None]
    if none_fields:
        raise Exception(f'Fields: {", ".join(none_fields)} is required')


def parse_body(body: json) -> dict:
    """Возвращает конвертированный в словарь json"""
    try:
        body = json.loads(body.decode('utf-8'))
    except json.JSONDecodeError:
        body = {}
    return body


def dict_fetchall(cursor) -> list:
    """Возвращает все строки результата запроса в виде списка словарей"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def fields_to_update(model):
    """Возвращает форматированную строку с указанными полями для запроса обновления"""
    lst = [f"{i} = '{model.__dict__[i]}'"
           for i in model.__dict__
           if i != 'id' and model.__dict__[i] is not None]
    return ", ".join(lst)


def fields_to_save(model):
    """Возвращает форматированную строку с указанными полями для запроса создания записи"""

    lst = [i
           for i in model.__dict__
           if model.__dict__[i] is not None]
    return ", ".join(lst)


def values_to_save(model):
    """Возвращает форматированную строку с указанными значениями полей для запроса создания записи"""
    lst = [f"'{str(model.__dict__[i])}'"
           for i in model.__dict__
           if model.__dict__[i] is not None]
    return ", ".join(lst)
