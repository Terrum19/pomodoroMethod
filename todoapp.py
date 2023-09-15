import random
import time

import flet as ft
import json
import random


class Todo_menu(ft.UserControl):
    def build(self):
        self.task_text_field = ft.TextField(
            hint_text='Добавьте таск: '
        )

        self.add_task_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=self.add_task, bgcolor=ft.colors.LIME_300
        )

        self.field_for_task_adding = ft.Row([
            self.task_text_field,
            self.add_task_button
        ])

        self.task_column = ft.Column()

        self.todo_menu = ft.Column([
            self.field_for_task_adding,
            self.task_column,
        ])

        return self.todo_menu

    def task_delete(self, task):
        self.task_column.controls.remove(task)
        self.update()

    def add_task(self, e):
        if self.task_text_field.value not in [list(elem.keys())[0] for elem in json.loads(
                open('todo_time_spent.json').read())] and self.task_text_field.value:
            task = Task(self.task_text_field.value, self.task_delete, False)
            overwrite_json = json.loads(open("todo_time_spent.json").read())
            overwrite_json.append({self.task_text_field.value:
                                       {"time_spent_on_task": 0, "is_activated": False, "will_render": True}})
            overwrite_json = json.dumps(overwrite_json)
            open('todo_time_spent.json', 'w').write(overwrite_json)
            self.task_column.controls.append(task)
            self.task_text_field.value = ''
            self.todo_menu.update()
        else:
            self.page.add(ft.SnackBar(ft.Text('Строка пуста или такое задание уже добавлено!'), open=True))


class Task(ft.UserControl):
    def __init__(self, task_name, task_delete, is_active):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete
        self.is_active = is_active

    def build(self):
        self.checkbox = ft.Checkbox(value=True if self.is_active else False, label=self.task_name,
                                    on_change=self.checkbox_state_change)
        self.edit_name = ft.TextField(hint_text='Что надо изменить?')

        self.edit_button = ft.FilledButton(
            text='Изменить',
            on_click=self.edit_clicked,
            col=ft.colors.GREEN
        )

        self.delete_button = ft.FilledButton(
            text='Удалить',
            on_click=self.delete_clicked,
            col=ft.colors.RED
        )

        self.save_button = ft.FilledButton(
            text='Сохранить',
            on_click=self.save_clicked,
            col=ft.colors.GREEN
        )

        self.task_view = ft.Row([
            self.checkbox,
            self.edit_button,
            self.delete_button
        ])

        self.task_edit = ft.Row([
            self.edit_name,
            self.save_button
        ],
            visible=False
        )

        self.task = ft.Column([
            self.task_view,
            self.task_edit
        ])

        return self.task

    def edit_clicked(self, e):
        self.edit_name.value = self.task_name
        self.task_view.visible = False
        self.task_edit.visible = True
        self.update()

    def save_clicked(self, e):
        json_changed = json.loads(open('todo_time_spent.json').read())
        json_replacer = []
        for task in json_changed:
            if list(task.keys())[0] == self.task_name:
                replace = {self.task_name: self.edit_name.value}
                json_replacer.append(dict((replace[key], value) for (key, value) in task.items()))
            else:
                json_replacer.append(task)
        open('todo_time_spent.json', 'w').write(json.dumps(json_replacer))
        self.checkbox.label = self.edit_name.value
        self.task_view.visible = True
        self.task_edit.visible = False
        self.update()

    def delete_clicked(self, e):
        json_changed = json.loads(open('todo_time_spent.json').read())
        for task in json_changed:
            if list(task.keys())[0] == self.task_name:
                task[self.task_name]['will_render'] = False
        open('todo_time_spent.json', 'w').write(json.dumps(json_changed))
        self.visible = False
        self.update()

    def checkbox_state_change(self, e):
        json_changed = json.loads(open('todo_time_spent.json').read())
        for task in json_changed:
            if list(task.keys())[0] == self.task_name:
                task[self.task_name]['is_activated'] = True if self.checkbox.value else False
        open('todo_time_spent.json', 'w').write(json.dumps(json_changed))

