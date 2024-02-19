import os
from tkinter.ttk import Style

import cv2
import numpy as np
from datetime import datetime, timedelta
import asyncio

from PIL import ImageTk, Image

from src.constant import app_title
from src.local import model_folder_path
from src.predict import predictImage
from src.train import train
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sv_ttk
from tkinter import ttk
from threading import Thread
from typing import Callable, List

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

        self.geometry("720x480")
        self.title(app_title)

        self.side_bar = ttk.Frame(self)
        self.side_bar.pack(anchor=tk.N, side=tk.LEFT)

        # Make the buttons with the icons to be shown
        self.make_model_b = ttk.Button(self.side_bar, text='모델 만들기', command=lambda: self.tab_selected(0),
                                       style='SideBar.TButton')
        self.make_model_b.pack(side=tk.TOP)

        self.predict_b = ttk.Button(self.side_bar, text='이미지 예측', command=lambda: self.tab_selected(1))
        self.predict_b.pack(side=tk.TOP)

        # content frame
        self.content_frame = tk.LabelFrame(self)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # tab1
        self.tab1 = MakeModelPage(self.content_frame)
        self.tab1.setup_ui(self)

        # tab2
        self.tab2 = PredictPage(self.content_frame)
        self.tab2.setup_ui(self)

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
            self.tab1.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        elif idx == 1:
            self.tab2.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)


class MakeModelPage(TabContent):

    def __init__(self, master):
        super().__init__(master)
        self.label = None
        self.path_label = None

        self.is_path_selected = False
        self.__path_label_text = ''

    @property
    def path_label_text(self):
        return self.__path_label_text

    @path_label_text.setter
    def path_label_text(self, value):
        self.__path_label_text = value
        self.is_path_selected = True
        self.path_label.config(text=value)

    def setup_ui(self, app):
        def choose_folder():
            folder_path = filedialog.askdirectory()
            if folder_path:
                self.path_label_text = folder_path

        self.title = ttk.Label(self, text="제품 이름을 입력해 주세요")
        self.title.pack(anchor=tk.W, pady=(20, 0), padx=20)

        self.entry = ttk.Entry(self)
        self.entry.pack(anchor=tk.W, pady=(5, 0), padx=20)

        self.label = ttk.Label(self, text="상품 이미지 경로를 선택해 주세요")
        self.label.pack(anchor=tk.W, pady=(15, 0), padx=20)

        self.path_label = ttk.Label(self, text="...")
        self.path_label.pack(anchor=tk.W, pady=(5, 0), padx=(20, 0))

        self.choose_b = ttk.Button(self, text='찾아보기', command=choose_folder)
        self.choose_b.pack(anchor=tk.W, pady=(5, 0), padx=(75, 0))

        self.train_button = ttk.Button(self,
                                       text="학습 시작",
                                       style='Accent.TButton',
                                       command=lambda: app.do_tasks(async_loop, self.start_training))
        self.train_button.pack(anchor=tk.W, padx=(73, 0), pady=(20, 0))

    async def start_training(self):
        await self.make_model()

    async def make_model(self):
        try:
            if not len(self.entry.get()):
                messagebox.showerror("실패", '상품 이름을 입력해 주세요')
                return
            if not self.is_path_selected:
                messagebox.showerror("실패", '상품 이미지 경로를 선택해 주세요')
                return
            model_path = train(product_name=self.entry.get(), input_path=self.label.cget('text'))
            print(model_path)
            messagebox.showinfo('성공', '모델 훈련이 완료되었습니다')
        except:
            messagebox.showerror('실패', '이미지 경로가 올바르지 않습니다')


class PredictPage(TabContent):

    def __init__(self, master):
        super().__init__(master)
        self.is_selected = False
        self.__selected_model_text = ""
        self.selected_model = None
        self.predict_button = None
        self.model_button_list: List[ttk.Button] = []

    @property
    def selected_model_text(self):
        return self.__selected_model_text

    @selected_model_text.setter
    def selected_model_text(self, selected_model_text):
        self.is_selected = True
        self.__selected_model_text = selected_model_text
        self.selected_model.configure(text='선택된 모델: ' + selected_model_text)

    def setup_ui(self, app):
        # 모델 이름 입력 필드
        self.selected_model = ttk.Label(self, text="모델을 선택해 주세요")
        self.selected_model.pack(anchor=tk.W, padx=(20, 0), pady=(20, 0))

        def on_click_model_button(model_path: str):
            self.selected_model_text = model_path

        for model_path in os.listdir(model_folder_path):

            model_button = ttk.Button(self, text=model_path, command=lambda: on_click_model_button(model_path))
            self.model_button_list.append(model_button)
            model_button.pack(anchor=tk.W, padx=(20, 0), pady=(5, 0))

        self.predict_button = ttk.Button(self, text="예측 시작",
                                         style='Accent.TButton',
                                         command=lambda: app.do_tasks(async_loop, self.start_predicting))
        self.predict_button.pack(anchor=tk.W, padx=(20, 0), pady=(20, 0))

        self.score_label = ttk.Label(self)
        self.score_label.pack()

        self.result_label = ttk.Label(self)
        self.result_label.pack()

        self.image = ttk.Label(self)
        self.image.pack()

    async def predict(self, model_name: str):
        while True:
            _, image = camera.read()

            score, result = predictImage(model_name=model_name, predict_image=image)
            photo = ImageTk.PhotoImage(Image.fromarray(image))
            self.image.config(image=photo)
            self.image.image = photo
            self.score_label.configure(text='정확도: ' + str(int(score * 100)) + '%')
            self.result_label.configure(text='결과: ' + '정상' if result else '불량')

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
        if not self.is_selected:
            messagebox.showerror("에러", "모델을 선택해 주세요.")
            return
        for model_button in self.model_button_list:
            model_button.pack_forget()
        await asyncio.gather(self.predict(self.selected_model_text), self.send_arduino())


async_loop = asyncio.get_event_loop()

# GUI 생성
app = App()
# app.attributes("-topmost", True)
sv_ttk.set_theme('light')
# app.update_idletasks()  # Make sure every screen redrawing is done
app.mainloop()
