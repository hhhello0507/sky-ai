import cv2
import numpy as np
from datetime import datetime, timedelta
import asyncio

from src.ai.ai import SkyAI
from src.model.store import Store
from src.util.arduino.arduino import SkyArduino

np.set_printoptions(suppress=True)
skyAI = SkyAI(model_path="../res/model/g_model.h5")
class_names = open("../labels.txt", "r").readlines()
store = Store(class_names=class_names)

camera = cv2.VideoCapture(1)
skyArduino = SkyArduino()


async def predict():
    while True:
        _, image = camera.read()

        skyAI.predict(image=image, output_store=store)
        cv2.waitKey(1)

        await asyncio.sleep(0.01)


async def sendArduino():
    before_time = datetime.now()
    while True:
        current_time = datetime.now()
        if before_time + timedelta(seconds=1) < current_time:
            mxIdx = store.get_max_index()
            skyArduino.send_classification_result(index=mxIdx)

            print(f"sended - mxIdx: {mxIdx}, encoded: {str(mxIdx).encode()}")

            before_time = current_time
            store.init_predict_store()
        await asyncio.sleep(0.01)


async def main():
    await asyncio.gather(predict(), sendArduino())


if __name__ == "__main__":
    asyncio.run(main())

    camera.release()
    cv2.destroyAllWindows()
