from tkinter.ttk import Style

import cv2
import numpy as np
from datetime import datetime, timedelta
import asyncio
from src.predict import predictImage
from src.train import train
import tkinter as tk
from tkinter import messagebox
import sv_ttk
from tkinter import ttk
from threading import Thread
from typing import Callable

np.set_printoptions(suppress=True)

camera = cv2.VideoCapture(1)


class TabContent(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

    def setup_ui(self, app):
        pass


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("400x300")
        self.title("Sky-AI")

        side_bar = ttk.Frame(self)
        side_bar.pack(anchor=tk.W, fill=tk.Y)

        # Make the buttons with the icons to be shown
        self.make_model_b = ttk.Button(side_bar, text='모델 만들기', command=lambda: self.tab_selected(0))
        self.make_model_b.pack(side=tk.TOP)

        self.predict_b = ttk.Button(side_bar, text='이미지 예측', command=lambda: self.tab_selected(1))
        self.predict_b.pack(side=tk.TOP)

        # content frame
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # tab1
        self.tab1 = MakeModelPage(self)
        self.tab1.setup_ui(self.content_frame)

        # tab2
        self.tab2 = PredictPage(self)
        self.tab2.setup_ui(self.content_frame)

        self.tab_selected(0)

    def _asyncio_thread(self, async_loop, task: Callable):
        async_loop.run_until_complete(task())

    def do_tasks(self, async_loop, task: Callable):
        if not asyncio.get_event_loop().is_running():
            Thread(target=self._asyncio_thread, args=(async_loop, task)).start()
        else:
            messagebox.showerror("에러", "이미 다른 작업이 실행중입니다")

    def tab_selected(self, idx):
        self.tab1.pack_forget()
        self.tab2.pack_forget()
        if idx == 0:
            self.tab1.pack(expand=True, fill=tk.BOTH)
        elif idx == 1:
            self.tab2.pack(expand=True, fill=tk.BOTH)


class MakeModelPage(TabContent):

    def setup_ui(self, app):
        self.train_button = ttk.Button(self, text="Train Model",
                                       command=lambda: app.do_tasks(async_loop, self.start_training))
        self.train_button.pack()

    async def start_training(self):
        await self.make_model()

    async def make_model(self):
        model_path = train(product_name='h', input_path='../res/data1')
        print(model_path)


class PredictPage(TabContent):

    def setup_ui(self, app):
        # 모델 이름 입력 필드
        self.model_name_label = ttk.Label(self, text="Model Name:")
        self.model_name_label.pack()
        self.model_name_entry = ttk.Entry(self)
        self.model_name_entry.pack()
        self.predict_button = ttk.Button(self, text="Start Prediction",
                                         command=lambda: app.do_tasks(async_loop, self.start_predicting))
        self.predict_button.pack()

    async def predict(self, model_name: str):
        while True:
            _, image = camera.read()

            predictImage(model_name=model_name, predict_image=image)

            # cv2.waitKey(1)
            await asyncio.sleep(0.5)

    async def send_arduino(self):
        before_time = datetime.now()
        while True:
            current_time = datetime.now()
            if before_time + timedelta(seconds=1) < current_time:
                # send
                print('send arduino')
                before_time = current_time
            await asyncio.sleep(0.5)

    async def start_predicting(self):
        model_name = self.model_name_entry.get()
        if not model_name:
            messagebox.showerror("에러", "모델 이름을 입력해 주세요.")
            return
        await asyncio.gather(self.predict(self.model_name_entry.get()), self.send_arduino())


async_loop = asyncio.get_event_loop()

# GUI 생성
app = App()
sv_ttk.set_theme('light')
app.mainloop()
