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

np.set_printoptions(suppress=True)

camera = cv2.VideoCapture(1)


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


async def main(mode):
    if mode == 0:
        # make model
        model_path = train(product_name='h', input_path='../res/data1')
        print(model_path)
    else:
        await asyncio.gather(predict(model_name_entry.get()), sendArduino())


def start_training():
    main(0)


def start_predicting():
    model_name = model_name_entry.get()
    if not model_name:
        messagebox.showerror("Error", "Please enter model name")
        return
    main(1)


# GUI 생성
root = tk.Tk()
root.title("Model Training and Prediction")

# 모델 이름 입력 필드
model_name_label = ttk.Label(root, text="Model Name:")
model_name_label.pack()
model_name_entry = ttk.Entry(root)
model_name_entry.pack()

# 버튼 생성
train_button = ttk.Button(root, text="Train Model", command=start_training)
train_button.pack()

predict_button = ttk.Button(root, text="Start Prediction", command=start_predicting)
predict_button.pack()

sv_ttk.set_theme('light')

root.mainloop()
