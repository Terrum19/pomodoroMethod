import json

import flet as ft
from os import getcwd
from os.path import exists
from timer import pomodoro_part
from todoapp import Todo_menu, Task

JSON_FILE_PATH = f'{getcwd()}\\todo_time_spent.json'
if not exists(JSON_FILE_PATH):
    todo_time_spent = open("todo_time_spent.json", 'w')
    todo_time_spent.write('[]')


def main(page: ft.Page):
    def json_tasks_load():
        for line in json.loads(open('todo_time_spent.json').read()):
            task_name = list(line.keys())[0]
            print(todo.todo_menu.controls)
            todo.todo_menu.controls[1].controls.append(Task(task_name, todo.task_delete))
            todo.update()

    page.theme_mode = ft.ThemeMode.DARK

    timer_app = pomodoro_part()
    todo = Todo_menu()

    page.add(ft.Row([timer_app, todo]))

    json_tasks_load()



ft.app(target=main)
