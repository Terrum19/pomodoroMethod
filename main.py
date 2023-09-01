import flet as ft
import time
from math import isclose, pi

from flet_core import RoundedRectangleBorder, Alignment


def main(page: ft.Page):
    def ringProgression(progressionSpeed, timer_time, start):
        progress_ring.color = ft.colors.WHITE
        progress_ring.value += 1 / (int(timer_time) * 60)
        progress_ring.update()
        pomodoro.rotate.angle += pi / 2
        pomodoro.update()
        time.sleep(progressionSpeed)
        elapsed_time.value = f'{(int(timer_time)*60 - (time.time() - start)) / 60}'
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

        pomodoro_button.disabled = True

        if working_loop:
            start = time.time()
            WORKTIME = int(work_time) * 60
            pomodoro_button.text = "Помидор запущен"
            pomodoro_button.update()
            for i in range(WORKTIME + 1):
                if isclose(progress_ring.value, 1):
                    ringReset(mode='work')
                else:
                    ringProgression(1, work_time, start)
        elif times_worked == 3:
            start = time.time()
            LONGCHILLTIME = int(longchill_time) * 60
            pomodoro_button.text = "Длительный отдых запущен"
            pomodoro_button.update()
            for i in range(LONGCHILLTIME + 1):
                if isclose(progress_ring.value, 1):
                    ringReset(mode='longchill')
                    times_worked = 0
                else:
                    ringProgression(1, longchill_time, start)
        elif not working_loop:
            start = time.time()
            CHILLTIME = int(chill_time) * 60
            pomodoro_button.text = "Отдых запущен"
            pomodoro_button.update()
            for i in range(CHILLTIME + 1):
                if isclose(progress_ring.value, 1):
                    ringReset(mode='chill')
                    times_worked += 1
                else:
                    ringProgression(1, chill_time, start)

    def change_time_variable(e):
        nonlocal work_time
        nonlocal chill_time
        nonlocal longchill_time
        nonlocal minutes_on_slider

        if dropdown_selector.value == 'work':
            work_time = slider.value
            minutes_on_slider.value = slider.value
        elif dropdown_selector.value == 'chill':
            chill_time = slider.value
            minutes_on_slider.value = slider.value
        else:
            longchill_time = slider.value
            minutes_on_slider.value = slider.value
        minutes_on_slider.update()


    def change_slider_value(e):
        if dropdown_selector.value == 'work':
            slider.value = work_time
        elif dropdown_selector.value == 'chill':
            slider.value = chill_time
        else:
            slider.value = longchill_time
        minutes_on_slider.value = slider.value
        minutes_on_slider.update()
        slider.update()

    page.fonts = {'Rodchenko': 'https://dropmefiles.com/xKKlG'}
    work_time = 0
    chill_time = 0
    longchill_time = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.title = 'Pomodoro Method'
    working_loop = True
    times_worked = 0

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

    elapsed_time = ft.Text(
        value='00:00',
        disabled=True,
        color=ft.colors.WHITE,
        scale=4,
        font_family='Rodchenko',
        right=time_container.width / 2 - 8,
        bottom=time_container.height / 2
    )

    timer = ft.Stack([
        time_container,
        elapsed_time
    ])

    slider = ft.Slider(
        min=5, max=60,
        divisions=11, scale=2,
        on_change=change_time_variable)

    worktime_option = ft.dropdown.Option(
        text='Настройка времени работы', key='work'
    )
    chill_option = ft.dropdown.Option(
        text='Настройка времени отдыха', key='chill'
    )
    longchill_option = ft.dropdown.Option(
        text='Настройка времени продолжительного отдыха', key='longchill'
    )

    minutes_on_slider = ft.Text(
        value='0'
    )

    dropdown_selector = ft.Dropdown(
        options=[
            worktime_option,
            chill_option,
            longchill_option
        ],
        width=400,
        on_change=change_slider_value
    )

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
            timer,
            ft.Row([
                pomodoro_button, pomodoro
            ],
                spacing=50
            ),
            pomodoro_stats,
            ft.Row([
                minutes_on_slider,
                slider,
            ], spacing=125),
            dropdown_selector
        ])
    ],
        spacing=0,
    )

    page.add(main_content)
    print(page)
    time.sleep(0.4)


ft.app(target=main)
