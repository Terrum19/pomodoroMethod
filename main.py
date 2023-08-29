import flet as ft
import time
from math import isclose, pi

from flet_core import RoundedRectangleBorder, Alignment


def main(page: ft.Page):
    def animate(e):
        pomodoro.offset = ft.transform.Offset(0, 0)
        pomodoro.update()

    def ringProgression(progressionSpeed, mode, start):
        progress_ring.color = ft.colors.WHITE
        progress_ring.value += 1 / (int(mode.value) * 60)
        progress_ring.update()
        pomodoro.rotate.angle += pi / 2
        pomodoro.update()
        time.sleep(progressionSpeed)
        elapsed_time.value = str(int(mode.value) * 60 - (time.time() - start))
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
                    ringProgression(0.01, working_time, start)
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
                    ringProgression(0.01, long_chill_time, start)

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
                    ringProgression(0.01, chill_time, start)



    page.theme_mode = ft.ThemeMode.DARK
    page.title = 'Pomodoro Method'
    working_loop = True
    times_worked = 0

    pomodoro = ft.Image(
        width=200,
        height=200,
        src='https://i.postimg.cc/JzZGs5sP/Removal-17.png',
        border_radius=5,
        offset=ft.transform.Offset(-2, 0),
        animate_offset=ft.animation.Animation(500),
        rotate=ft.transform.Rotate(0, alignment=ft.alignment.center),
        animate_rotation=ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT),
    )

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
        width=100
    )

    stacked_ring = ft.Stack([
        time_container,
        elapsed_time
    ]
    )

    working_time = ft.TextField(hint_text="Введите время работы(в минутах)")
    chill_time = ft.TextField(hint_text='Введите время отдыха(в минутах)')
    long_chill_time = ft.TextField(hint_text='Введите время продолжительного отдыха(в минутах)')

    minus = ft.IconButton(
        icon=ft.icons.EXPOSURE_MINUS_1_SHARP
    )

    plus = ft.IconButton(
        icon=ft.icons.PLUS_ONE_SHARP
    )

    pomodoro_stats = ft.Row([
        time_container,
        ft.Column([
            ft.TextField(value='Помидоров прошло: '),
            ft.Row([
                minus,
                ft.TextField(value='Помидоров пропущено: '),
                plus
            ])

        ])

    ])

    users_wishes = ft.Row([
        working_time,
        chill_time,
        long_chill_time
    ])

    page.add(pomodoro_stats, e;)

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

    page.add(pomodoro_button, users_wishes, pomodoro)
    time.sleep(0.4)
    animate(pomodoro)


ft.app(target=main)
