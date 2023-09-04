import flet as ft
from timer import pomodoro_part
from todoapp import Todo_menu

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK

    timer_app = pomodoro_part()
    todo = Todo_menu()

    page.add(ft.Row([timer_app, todo]))


ft.app(target=main)
