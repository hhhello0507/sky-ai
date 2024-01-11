from datetime import datetime, timedelta
import os

import cv2
import numpy as np

from src.ai.ai import SkyAI
from src.model.store import Store
from src.util.arduino.arduino import SkyArduino

from src.view.main_view import MainView


def predict():
    _, image = camera.read()

    skyAI.predict(image=image, output_store=store)
    cv2.waitKey(1)


def sendArduino():
    global before_time
    current_time = datetime.now()
    if before_time + timedelta(seconds=1) < current_time:
        mxIdx = store.get_max_index()
        skyArduino.send_classification_result(index=mxIdx)

        print(f"sended - mxIdx: {mxIdx}, encoded: {str(mxIdx).encode()}")

        before_time = current_time
        store.init_predict_store()


def view():
    main_view = MainView(title='AI')
    main_view.init_view()
    root = main_view.get_root()
    root.after(10, predict)
    root.after(10, sendArduino)
    root.mainloop()


if __name__ == "__main__":
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    np.set_printoptions(suppress=True)
    skyAI = SkyAI(model_path="../res/model/g_model.h5")
    class_names = open("../labels.txt", "r").readlines()
    store = Store(class_names=class_names)

    camera = cv2.VideoCapture(1)
    skyArduino = SkyArduino()
    before_time = datetime.now()

    view()
    # asyncio.run(ai())
    camera.release()
    cv2.destroyAllWindows()
