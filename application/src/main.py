import cv2
import numpy as np
from datetime import datetime, timedelta
import asyncio

np.set_printoptions(suppress=True)

camera = cv2.VideoCapture(1)


async def predict():
    while True:
        _, image = camera.read()

        

        cv2.waitKey(1)
        await asyncio.sleep(0.01)


async def sendArduino():
    before_time = datetime.now()
    while True:
        current_time = datetime.now()
        if before_time + timedelta(seconds=1) < current_time:
            # send
            before_time = current_time
        await asyncio.sleep(0.01)


async def main():
    await asyncio.gather(predict(), sendArduino())


if __name__ == "__main__":
    asyncio.run(main())

    camera.release()
    cv2.destroyAllWindows()
