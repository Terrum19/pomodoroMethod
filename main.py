import flet as ft
import time
from math import isclose, pi

from flet_core import RoundedRectangleBorder, Alignment


def main(page: ft.Page):
    def ringProgression(progressionSpeed, mode, start):
        progress_ring.color = ft.colors.WHITE
        progress_ring.value += 1 / (int(mode.value) * 60)
        progress_ring.update()
        pomodoro.rotate.angle += pi / 2
        pomodoro.update()
        time.sleep(progressionSpeed)
        elapsed_time.value = round(int(int(mode.value) * 60 - (time.time() - start)) / 60, 1)
        elapsed_time.update()

    def ringReset(mode):
        nonlocal working_loop
        nonlocal times_worked

        i = 0.001
        progress_ring.color = ft.colors.GREEN
        progress_ring.update()
        while progress_ring.value > 0:
            progress_ring.value -= i
            progress_ring.update()
            elapsed_time.value = progress_ring.value
            elapsed_time.update()
            time.sleep(0.01)
            i += 0.0001
        progress_ring.value = 0
        pomodoro_button.disabled = False
        working_loop = True if mode == 'chill' else False
        match mode:
            case 'chill':
                pomodoro_button.text = 'Начать работу'
            case 'work':
                pomodoro_button.text = 'Начать отдых' if times_worked != 3 else "Начать продолжительный отдых"
            case 'longchill':
                pomodoro_button.text = 'Начать работу'
        pomodoro_button.update()

    def buttonProgressionStart(e):
        nonlocal working_loop
        nonlocal times_worked

        try:
            int(working_time.value)
            pomodoro_button.disabled = True

            if working_loop:
                start = time.time()
                WORKTIME = int(working_time.value) * 60

                pomodoro_button.text = "Помидор запущен"
                pomodoro_button.update()

                for i in range(WORKTIME + 1):
                    if isclose(progress_ring.value, 1):
                        ringReset(mode='work')
                    else:
                        ringProgression(1, working_time, start)
            elif times_worked == 3:
                start = time.time()
                LONGCHILLTIME = int(long_chill_time.value) * 60

                pomodoro_button.text = "Длительный отдых запущен"
                pomodoro_button.update()

                for i in range(LONGCHILLTIME + 1):
                    if isclose(progress_ring.value, 1):
                        ringReset(mode='longchill')
                        times_worked = 0
                    else:
                        ringProgression(1, long_chill_time, start)

            elif not working_loop:
                start = time.time()
                CHILLTIME = int(chill_time.value) * 60

                pomodoro_button.text = "Отдых запущен"
                pomodoro_button.update()

                for i in range(CHILLTIME + 1):
                    if isclose(progress_ring.value, 1):
                        ringReset(mode='chill')
                        times_worked += 1
                    else:
                        ringProgression(1, chill_time, start)
        except ValueError:
            open_dlg(e)


    page.theme_mode = ft.ThemeMode.DARK
    page.title = 'Pomodoro Method'
    working_loop = True
    times_worked = 0

    alert = ft.AlertDialog(
        title=ft.Text('Некорректно введено поле'),
            )

    def open_dlg(e):
        page.dialog = alert
        alert.open = True
        page.update()

    pomodoro = ft.Image(
        width=70,
        height=70,
        src='https://i.postimg.cc/JzZGs5sP/Removal-17.png',
        border_radius=5,
        rotate=ft.transform.Rotate(0, alignment=ft.alignment.center),
        animate_rotation=ft.Animation(500, ft.AnimationCurve.BOUNCE_IN)
    )

    pomodoro_button = ft.ElevatedButton(
        text="Запустить помидор",
        autofocus=True,
        on_click=buttonProgressionStart,
        style=ft.ButtonStyle(
            shape={
                ft.MaterialState.HOVERED: RoundedRectangleBorder(radius=20),
                ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)
            },
            bgcolor='#F50A0A'
        ))

    progress_ring = ft.ProgressRing(
        width=300, height=300, stroke_width=9, value=0,
    )

    time_container = ft.Container(
        content=progress_ring,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=Alignment(0, 0.7),
            colors=[
                '#020024',
                '#1f2b30',
                "#622d73"
            ]
        ),
        bgcolor=ft.colors.GREY_900,
        padding=12,
        width=320,
        height=320,
        border_radius=60,
        alignment=ft.alignment.center
    )

    elapsed_time = ft.TextField(
        value='0',
        disabled=True,
        width=100,
        color=ft.colors.WHITE
    )

    elapsed_time_container = ft.Container(
        content=elapsed_time,
        gradient=ft.LinearGradient(
            colors=[
                "#250902",
                "#38040e",
                "#640d14",
                "#800e13",
                "#ad2831"
            ],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_center
        ),
        border_radius=10
    )

    working_time = ft.TextField(
        hint_text="Введите время работы(в минутах)",
        keyboard_type=ft.KeyboardType.NUMBER)
    chill_time = ft.TextField(
        hint_text='Введите время отдыха(в минутах)',
        keyboard_type=ft.KeyboardType.NUMBER)
    long_chill_time = ft.TextField(
        hint_text='Введите время продолжительного отдыха(в минутах)',
        keyboard_type=ft.KeyboardType.NUMBER)


    minus = ft.IconButton(
        icon=ft.icons.EXPOSURE_MINUS_1_SHARP
    )

    plus = ft.IconButton(
        icon=ft.icons.PLUS_ONE_SHARP
    )

    pomodoro_stats = ft.Row([
        ft.Column([
            ft.Row([
                minus,
                ft.TextField(value='Помидоров пройдено: '),
                plus
            ])
        ])
    ])

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        height=400,
        leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.FAVORITE_BORDER, selected_icon=ft.icons.FAVORITE, label="First"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                label="Second",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Settings"),
            ),
        ],
    )

    main_content = ft.Row([
        rail,
        ft.VerticalDivider(color='green'),
        ft.Column([
            time_container,
            ft.Row([
                pomodoro_button, elapsed_time_container, pomodoro
            ],
                spacing=50
            ),
            pomodoro_stats,
            working_time,
            chill_time,
            long_chill_time
        ])
    ],
        spacing=0,
    )

    page.add(main_content)
    print(page)
    time.sleep(0.4)


ft.app(target=main)
