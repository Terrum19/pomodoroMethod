import flet as ft
import json

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
            self.task_column
        ])

        return self.todo_menu

    def task_delete(self, task):
        self.task_column.controls.remove(task)
        self.update()

    def add_task(self, e):
        if self.task_text_field.value not in open("todo_time_spent.json").read():
            print(json.loads(open("todo_time_spent.json").read()))
            overwrite_json = json.loads(open("todo_time_spent.json").read())
            overwrite_json.append({self.task_text_field.value: [{"time_spent_on_task": 0}, {"is_activated": False}]})
            overwrite_json = json.dumps(overwrite_json)
            open('todo_time_spent.json', 'w').write(overwrite_json)


        if self.task_text_field.value != '':
            task = Task(self.task_text_field.value, self.task_delete)
            self.task_column.controls.append(task)
            self.task_text_field.value = ''
            self.todo_menu.update()
            print(self.task_column.controls[0])


class Task(ft.UserControl):
    def __init__(self, task_name, task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):
        self.checkbox = ft.Checkbox(value=False, label=self.task_name)
        self.edit_name = ft.TextField(hint_text='Что надо изменить?')

        self.edit_button = ft.FilledButton(
            text='Изменить',
            on_click=self.edit_clicked,
            col=ft.colors.GREEN
        )

        self.delete_button = ft.FilledButton(
            text='Удалить',
            on_click=self.task_delete,
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
        print(open('todo_time_spent.json').read().find())
        self.checkbox.label = self.edit_name.value
        self.task_view.visible = True
        self.task_edit.visible = False
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)



