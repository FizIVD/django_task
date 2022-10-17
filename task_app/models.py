from task_app.utils import validate, fields_to_update, fields_to_save, values_to_save, dict_fetchall
import psycopg2
from django.db import connection


class Model:
    table: str
    id: int

    def get(self):
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.table} WHERE id = {self.id};")
            data = cursor.fetchone()
            if not data:
                raise Exception(f'ID {self.id} does not exist')
            return data
        except (Exception, psycopg2.Error) as error:
            raise Exception(error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()

    def update(self):
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.table} WHERE id = {self.id};")
            item_exist = cursor.fetchone()
            if not item_exist:
                raise Exception(f'ID {self.id} does not exist')
            cursor.execute(f"UPDATE {self.table} SET {fields_to_update(self)}  WHERE id = {self.id} RETURNING id;")
            self.id = cursor.fetchone()[0]
            return self.id
        except (Exception, psycopg2.Error) as error:
            raise Exception(error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()

    def save(self):
        cursor = connection.cursor()
        try:
            cursor.execute(f"INSERT INTO {self.table} ({fields_to_save(self)}) VALUES ({values_to_save(self)}) RETURNING id;")
            self.id = cursor.fetchone()[0]
            return self.id
        except (Exception, psycopg2.Error) as error:
            raise Exception(error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()

    def delete(self):
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.table} WHERE id = {self.id};")
            item_exist = cursor.fetchone()
            if not item_exist:
                raise Exception(f'ID {self.id} does not exist')
            cursor.execute(f"DELETE FROM {self.table} WHERE id = {self.id} RETURNING id;")
            self.id = cursor.fetchone()[0]
            return self.id
        except (Exception, psycopg2.Error) as error:
            raise Exception(error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()

    def is_valid_delete(self):
        validate(id=self.id)

    def is_valid_update(self):
        validate(id=self.id)


class Position(Model):
    table = 'pos'
    id: int
    position: str
    category: str

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.position = kwargs.get("position", None)
        self.category = kwargs.get("category", None)

    def load(self):
        if self.id:
            try:
                data = self.get()
                self.position = data[0]
                self.id = data[1]
                self.category = data[2]
            except (Exception, psycopg2.Error) as error:
                raise Exception(error)
        else:
            raise Exception('id not defined')

    def check_staff(self):
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM staff WHERE position = {self.id};")
            staff_list = dict_fetchall(cursor)
            r = [i.get('full_name') for i in staff_list]
            if staff_list:
                print(staff_list)
                raise Exception(f'Current staff:{r} have this position')
        except (Exception, psycopg2.Error) as error:
            raise Exception(error)

    def is_valid_create(self):
        validate(position=self.position, category=self.category)

    def __str__(self):
        return f'{self.id if self.id else None} {self.position} {self.category}'


class Staff(Model):
    table = 'staff'
    id: int
    full_name: str
    gender: str
    age: int
    position: int

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.full_name = kwargs.get("full_name", None)
        self.gender = kwargs.get("gender", None)
        self.age = kwargs.get("age", None)
        self.position = kwargs.get("position", None)

    def load(self):
        if self.id:
            try:
                data = self.get()
                self.full_name = data[0]
                self.age = data[1]
                self.position = data[2]
                self.id = data[3]
                self.gender = data[4]
            except (Exception, psycopg2.Error) as error:
                raise Exception(error)
        else:
            raise Exception('id not defined')

    def is_valid_create(self):
        validate(full_name=self.full_name, gender=self.gender, age=self.age, position=self.position)

    def __str__(self):
        return f'{self.id if self.id else None} {self.full_name} {self.gender} {self.age} {self.position}'
