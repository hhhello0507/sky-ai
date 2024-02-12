import cv2
import numpy as np
from datetime import datetime, timedelta
import asyncio
from src.predict import predictImage
from src.train import train

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


async def main():
    mode = int(input("0: make model\n1: predict model\n"))
    if not mode:
        # make model
        model_path = train(product_name='h', input_path='../res/data1')
        print(model_path)
    else:
        model_name = input("Enter model name\n")
        await asyncio.gather(predict(model_name), sendArduino())


if __name__ == "__main__":
    asyncio.run(main())

    # camera.release()
    # cv2.destroyAllWindows()
