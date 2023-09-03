import flet as ft
from timer import pomodoro_part

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    timer_app = pomodoro_part()
    page.add(ft.Row([
        timer_app,
        ft.VerticalDivider(width=9, thickness=3),
    ]))


ft.app(target=main)
