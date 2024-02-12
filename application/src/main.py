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


def _asyncio_thread(async_loop, task: Callable):
    async_loop.run_until_complete(task())


def do_tasks(async_loop, task: Callable):
    if not asyncio.get_event_loop().is_running():
        Thread(target=_asyncio_thread, args=(async_loop, task)).start()
    else:
        messagebox.showerror("에러", "이미 다른 작업이 실행중입니다")


async def predict(model_name: str):
    while True:
        _, image = camera.read()

        predictImage(model_name=model_name, predict_image=image)

        # cv2.waitKey(1)
        await asyncio.sleep(0.5)


async def sendArduino():
    before_time = datetime.now()
    while True:
        current_time = datetime.now()
        if before_time + timedelta(seconds=1) < current_time:
            # send
            print('send arduino')
            before_time = current_time
        await asyncio.sleep(0.5)


async def on_start(mode):
    if mode == 0:
        # make model
        model_path = train(product_name='h', input_path='../res/data1')
        print(model_path)
    else:
        await asyncio.gather(predict(model_name_entry.get()), sendArduino())


async def start_training():
    await on_start(0)


async def start_predicting():
    model_name = model_name_entry.get()
    if not model_name:
        messagebox.showerror("에러", "모델 이름을 입력해 주세요.")
        return
    await on_start(1)


async_loop = asyncio.get_event_loop()

# GUI 생성
root = tk.Tk()
root.title("Model Training and Prediction")

# 모델 이름 입력 필드
model_name_label = ttk.Label(root, text="Model Name:")
model_name_label.pack()
model_name_entry = ttk.Entry(root)
model_name_entry.pack()

# 버튼 생성
train_button = ttk.Button(root, text="Train Model", command=lambda: do_tasks(async_loop, start_training))
train_button.pack()

predict_button = ttk.Button(root, text="Start Prediction", command=lambda: do_tasks(async_loop, start_predicting))
predict_button.pack()

sv_ttk.set_theme('light')

root.mainloop()

