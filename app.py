import json

import flet as ft
from os import getcwd
from os.path import exists
from timer import PomodoroPart
from todoapp import TodoMenu, Task

"""
Creating a JSON file, that will storage all the tasks
if program is opened for the first time or JSON is empty
"""
JSON_FILE_PATH = f'{getcwd()}\\todo_time_spent.json'
if not exists(JSON_FILE_PATH):
    todo_time_spent = open("todo_time_spent.json", 'w')
    todo_time_spent.write('[]')
elif open('todo_time_spent.json').read() == '':
    open('todo_time_spent.json', 'w').write('[]')

def main(page: ft.Page):
    """
    A function that loads all saved tasks from JSON file
    and adds them on the screen
    """
    def json_tasks_load():
        for line in json.loads(open('todo_time_spent.json').read()):
            if line[list(line.keys())[0]]['will_render'] == True:
                task_name = list(line.keys())[0]
                checked = line[task_name]['is_activated']
                todo.todo_menu.controls[1].controls.append(Task(task_name, todo.task_delete, checked))
                todo.update()

    page.theme_mode = ft.ThemeMode.DARK

    timer_app = PomodoroPart()
    todo = TodoMenu()

    page.add(ft.Row([timer_app, todo]))
    json_tasks_load()


ft.app(target=main)
