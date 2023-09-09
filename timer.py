import flet as ft
from flet_core import RoundedRectangleBorder, Alignment
import time
from math import isclose, pi
import json


class pomodoro_part(ft.UserControl):
    def build(self):
        self.work_time = 5
        self.chill_time = 5
        self.longchill_time = 5
        self.working_loop = True
        self.times_till_longchill = 0
        self.times_worked = 0
        self.is_audio_added = False
        self.mode = 'work'
        self.reset_state = True
        self.json_config = json.loads(open('todo_time_spent.json').read())
        self.task_list = [list(element.keys())[0] for element in self.json_config
                     if element[list(element.keys())[0]]['is_activated']]

        self.audio1 = ft.Audio(
            src="https://luan.xyz/files/audio/ambient_c_motion.mp3"
        )

        self.pomodoro_button = ft.ElevatedButton(
            text="Запустить помидор",
            autofocus=True,
            on_click=self.buttonProgressionStart,
            style=ft.ButtonStyle(
                shape={
                    ft.MaterialState.HOVERED: RoundedRectangleBorder(radius=20),
                    ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)
                },
                bgcolor='#F50A0A'
            ))



        self.progress_ring = ft.ProgressRing(
            width=300, height=300, stroke_width=9, value=0,
        )

        self.time_container = ft.Container(
            content=self.progress_ring,
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

        self.pomodoro = ft.Image(
            width=70,
            height=70,
            src='https://i.postimg.cc/JzZGs5sP/Removal-17.png',
            border_radius=5,
            rotate=ft.transform.Rotate(0, alignment=ft.alignment.center),
            animate_rotation=ft.Animation(500, ft.AnimationCurve.BOUNCE_IN),
            left=self.time_container.width / 2 - 45,
            bottom=self.time_container.height / 5
        )

        self.elapsed_time = ft.Text(
            value='00:00',
            disabled=True,
            color=ft.colors.WHITE,
            scale=4,
            font_family='Rodchenko',
            right=self.time_container.width / 2 - 8,
            bottom=self.time_container.height / 2
        )

        self.timer = ft.Stack([
            self.time_container,
            self.elapsed_time,
            self.pomodoro
        ])

        self.slider = ft.Slider(
            min=5, max=60,
            divisions=11, scale=2,
            on_change=self.change_time_variable)

        self.worktime_option = ft.dropdown.Option(
            text='Настройка времени работы', key='work'
        )
        self.chill_option = ft.dropdown.Option(
            text='Настройка времени отдыха', key='chill'
        )
        self.longchill_option = ft.dropdown.Option(
            text='Настройка времени продолжительного отдыха', key='longchill'
        )

        self.minutes_on_slider = ft.Text(
            value='0'
        )

        self.dropdown_selector = ft.Dropdown(
            options=[
                self.worktime_option,
                self.chill_option,
                self.longchill_option
            ],
            width=400,
            on_change=self.change_slider_value
        )

        self.dropdown_selector.value = 'work'

        self.minus = ft.IconButton(
            icon=ft.icons.EXPOSURE_MINUS_1_SHARP
        )

        self.plus = ft.IconButton(
            icon=ft.icons.PLUS_ONE_SHARP
        )

        self.pomodoro_stats = ft.Row([
            self.minus,
            ft.TextField(value='Помидоров пройдено: '),
            self.plus
        ])

        self.passed_time_column = ft.Column()

        self.main_content = ft.Row([
            ft.Column([
                ft.Row([
                    self.timer,
                    ft.VerticalDivider(),
                ],
                    spacing=70
                ),
                self.pomodoro_button,
                self.pomodoro_stats,
                ft.Row([
                    self.minutes_on_slider,
                    self.slider,
                ], spacing=125),
                self.dropdown_selector,
                self.passed_time_column
            ]),
        ],
            spacing=0,
        )

        return self.main_content

    def time_spent_updater(self):
        self.passed_time_column.clean()
        json_changed = json.loads(open('todo_time_spent.json').read())
        for task in json_changed:
            hours = task[list(task.keys())[0]]["time_spent_on_task"] // 60 // 60
            minutes = (task[list(task.keys())[0]]["time_spent_on_task"] - hours * 60 * 60) // 60
            seconds = task[list(task.keys())[0]]["time_spent_on_task"] - hours * 60 * 60 - minutes * 60
            if task[list(task.keys())[0]]['will_render'] and task[list(task.keys())[0]]:
                self.passed_time_column.controls.append(
                    ft.Text(value=f'{list(task.keys())[0]} = {hours} часов, {minutes} минут, {seconds} секунд'))
                self.passed_time_column.update()

    def ringProgression(self, progressionSpeed, timer_time, start):
        minutes = '{:02d}'.format(round(timer_time * 60 - (time.time() - start)) // 60)
        seconds = '{:02d}'.format(round((timer_time * 60 - (time.time() - start)) % 60))
        self.progress_ring.color = ft.colors.WHITE
        self.progress_ring.value += 1 / (int(timer_time) * 60)
        self.progress_ring.update()
        self.pomodoro.rotate.angle += pi / 2
        self.pomodoro.update()
        self.time_spent_updater()
        time.sleep(progressionSpeed)
        self.json_task_time_adder(task_list=self.task_list, time_to_add=1)
        self.elapsed_time.value = f"{minutes}:{seconds}"
        self.elapsed_time.update()

    def ringReset(self, mode):
        self.main_content.controls[1].seek(0)
        self.main_content.controls[1].play()

        i = 0.001
        self.progress_ring.color = ft.colors.GREEN
        self.progress_ring.update()
        while self.progress_ring.value > 0:
            self.progress_ring.value -= i
            self.progress_ring.update()
            time.sleep(0.01)
            i += 0.0001
        self.progress_ring.value = 0
        self.pomodoro_button.disabled = False
        self.working_loop = True if mode == 'chill' else False
        match mode:
            case 'chill':
                self.pomodoro_button.text = 'Начать работу'
            case 'work':
                self.pomodoro_button.text = 'Начать отдых' if self.times_till_longchill != 3 else "Начать продолжительный отдых"
            case 'longchill':
                self.pomodoro_button.text = 'Начать работу'
        self.pomodoro_button.update()
        self.slider.disabled = False
        self.slider.update()

    def buttonProgressionStart(self, e):
        self.slider.disabled = True
        self.reset_state = True if not self.reset_state else False
        self.slider.update()

        if not self.is_audio_added:
            self.main_content.controls.append(self.audio1)
            self.main_content.update()
            self.is_audio_added = True
        else:
            self.main_content.controls[1].pause()
            self.main_content.update()

        if self.working_loop:
            start = time.time()
            WORKTIME = int(self.work_time) * 60
            self.mode = 'work'
            self.pomodoro_button.text = "Помидор запущен\n  Прервать?"
            self.pomodoro_button.update()
            for i in range(WORKTIME + 1):
                if isclose(self.progress_ring.value, 1):
                    self.ringReset('work')
                elif self.reset_state:
                    self.ringReset('chill')
                    return
                else:
                    self.ringProgression(1, self.work_time, start)
        elif self.times_till_longchill == 3:
            start = time.time()
            self.pomodoro_button.disabled = True
            LONGCHILLTIME = int(self.longchill_time) * 60
            self.mode = 'longchill'
            self.pomodoro_button.text = "Длительный отдых запущен"
            self.pomodoro_button.update()
            for i in range(LONGCHILLTIME + 1):
                if isclose(self.progress_ring.value, 1):
                    self.ringReset('longchill')
                    self.times_till_longchill = 0
                else:
                    self.ringProgression(1, self.longchill_time, start)
        elif not self.working_loop:
            start = time.time()
            CHILLTIME = int(self.chill_time) * 60
            self.pomodoro_button.disabled = True
            self.mode = 'chill'
            self.pomodoro_button.text = "Отдых запущен"
            self.pomodoro_button.update()
            for i in range(CHILLTIME + 1):
                if isclose(self.progress_ring.value, 1):
                    self.ringReset('chill')
                    self.times_till_longchill += 1
                    self.times_worked += 1
                    self.pomodoro_stats.controls[1].value = f"Помидоров пройдено: {self.times_worked}"
                    self.pomodoro_stats.update()
                else:
                    self.ringProgression(1, self.chill_time, start)

    def change_time_variable(self, e):
        if self.dropdown_selector.value == 'work':
            self.work_time = self.slider.value
            self.minutes_on_slider.value = self.slider.value
        elif self.dropdown_selector.value == 'chill':
            self.chill_time = self.slider.value
            self.minutes_on_slider.value = self.slider.value
        else:
            self.longchill_time = self.slider.value
            self.minutes_on_slider.value = self.slider.value
        self.minutes_on_slider.update()

    def change_slider_value(self, e):
        if self.dropdown_selector.value == 'work':
            self.slider.value = self.work_time
        elif self.dropdown_selector.value == 'chill':
            self.slider.value = self.chill_time
        else:
            self.slider.value = self.longchill_time
        self.minutes_on_slider.value = self.slider.value
        self.minutes_on_slider.update()
        self.slider.update()

    def json_task_time_adder(self, task_list, time_to_add):
        json_changed = json.loads(open('todo_time_spent.json').read())
        for task in json_changed:
            if list(task.keys())[0] in task_list:
                task[list(task.keys())[0]]['time_spent_on_task'] += time_to_add
        open('todo_time_spent.json', 'w').write(json.dumps(json_changed))
