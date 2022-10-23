import json
from typing import Any
import psycopg2
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from task_app.models import Position, Staff
from task_app.utils import dict_fetchall, parse_body


def staff(request: Any) -> HttpResponse:
    """Возвращает json Cписок сотрудников"""
    if request.method == 'GET':
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT s.id, full_name, gender, age, p.position, p.category "
                           "FROM staff s left join pos p on s.position=p.id ORDER BY full_name;")
            r = dict_fetchall(cursor)
            return HttpResponse(json.dumps(r))
        except (Exception, psycopg2.Error) as error:
            return HttpResponse(json.dumps({'error': str(error)}))
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
    else:
        return HttpResponse(json.dumps({'error': 'Only GET method allowed!'}))


def positions(request: Any) -> HttpResponse:
    """Возвращает json Cписок должностей и соответствующих категорий"""
    if request.method == 'GET':
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT id, position, category FROM pos ORDER BY position;")
            r = dict_fetchall(cursor)
            return HttpResponse(json.dumps(r))
        except (Exception, psycopg2.Error) as error:
            return HttpResponse(json.dumps({'error': str(error)}))
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
    else:
        return HttpResponse(json.dumps({'error': 'Only GET method allowed!'}))


@csrf_exempt
def get_position(request: Any) -> HttpResponse:
    """Возвращает json Данные сотрудника"""
    if request.method == 'POST':
        try:
            position = Position(**parse_body(request.body))
            position.load()
            return HttpResponse(json.dumps(position.__dict__))
        except Exception as e:
            return HttpResponse(json.dumps({'error': str(e)}))
    else:
        return HttpResponse(json.dumps({'error': 'Only POST method allowed!'}))


@csrf_exempt
def create_position(request: Any) -> HttpResponse:
    """Возвращает json созданной должности"""
    if request.method == 'POST':
        try:
            position = Position(**parse_body(request.body))
            position.is_valid_create()
            position.save()
            return HttpResponse(json.dumps(position.__dict__))
        except Exception as e:
            return HttpResponse(json.dumps({'error': str(e)}))
    else:
        return HttpResponse(json.dumps({'error': 'Only POST method allowed!'}))


@csrf_exempt
def del_position(request: Any) -> HttpResponse:
    """Возвращает json id удаленной должности"""
    if request.method == 'DELETE':
        try:
            position = Position(**parse_body(request.body))
            position.is_valid_delete()
            position.check_staff()
            position.delete()
            return HttpResponse(json.dumps({'id': position.id}))
        except Exception as e:
            return HttpResponse(json.dumps({'error': str(e)}))
    else:
        return HttpResponse(json.dumps({'error': 'Only DELETE method allowed!'}))


@csrf_exempt
def update_position(request: Any) -> HttpResponse:
    """Возвращает json: id обновленной должности например"""
    if request.method == 'PATCH':
        try:
            position = Position(**parse_body(request.body))
            position.is_valid_update()
            position.update()
            return HttpResponse(json.dumps({'id': position.id}))
        except Exception as e:
            return HttpResponse(json.dumps({'error': str(e)}))
    else:
        return HttpResponse(json.dumps({'error': 'Only PATCH method allowed!'}))


@csrf_exempt
def get_employee(request: Any) -> HttpResponse:
    """Возвращает json Данные сотрудника"""
    if request.method == 'POST':
        try:
            staff = Staff(**parse_body(request.body))
            staff.load()
            return HttpResponse(json.dumps(staff.__dict__))
        except Exception as e:
            return HttpResponse(json.dumps({'error': str(e)}))
    else:
        return HttpResponse(json.dumps({'error': 'Only POST method allowed!'}))


@csrf_exempt
def create_employee(request: Any) -> HttpResponse:
    """Возвращает json данные созданного сотрудника"""
    if request.method == 'POST':
        try:
            employee = Staff(**parse_body(request.body))
            employee.is_valid_create()
            employee.save()
            return HttpResponse(json.dumps(employee.__dict__))
        except Exception as e:
            return HttpResponse(json.dumps({'error': str(e)}))
    else:
        return HttpResponse(json.dumps({'error': 'Only POST method allowed!'}))


@csrf_exempt
def del_employee(request: Any) -> HttpResponse:
    """Возвращает json id удаленного сотрудника"""
    if request.method == 'DELETE':
        try:
            employee = Staff(**parse_body(request.body))
            employee.is_valid_delete()
            employee.delete()
            return HttpResponse(json.dumps({'id': employee.id}))
        except Exception as e:
            return HttpResponse(json.dumps({'error': str(e)}))
    else:
        return HttpResponse(json.dumps({'error': 'Only DELETE method allowed!'}))


@csrf_exempt
def update_employee(request: Any) -> HttpResponse:
    """Возвращает json: id обновленной записи сотрудника"""
    if request.method == 'PATCH':
        try:
            employee = Staff(**parse_body(request.body))
            employee.is_valid_update()
            employee.update()
            return HttpResponse(json.dumps({'id': employee.id}))
        except Exception as e:
            return HttpResponse(json.dumps({'error': str(e)}))
    else:
        return HttpResponse(json.dumps({'error': 'Only PATCH method allowed!'}))


def render_index(request):
    """Генерирует страницу "Список сотрудников" """
    return render(request=request, template_name='task/staff.html')


def render_positions(request):
    """Генерирует страницу "Список должностей" """
    return render(request=request, template_name='task/positions.html')


def render_create_employee(request):
    """Генерирует страницу "Добавление сотрудника" """
    return render(request=request, template_name='task/create_employee.html')


def render_edit_employee(request):
    """Генерирует страницу "Личная карточка сотрудника" """
    return render(request=request, template_name='task/edit_employee.html')


def render_edit_position(request):
    """Генерирует страницу "Изменение должности" """
    return render(request=request, template_name='task/edit_position.html')


def render_create_position(request):
    """Генерирует страницу "Новая должность" """
    return render(request=request, template_name='task/create_position.html')
