import cv2
import numpy as np
from keras.models import load_model

from src.model.store import Store


class SkyAI:

    def __init__(self, model_path):
        self.model = load_model(model_path, compile=False)

    def predict(self, image, output_store: Store):

        image = self._get_prepared_image(image)

        prediction = self.model.predict(image, verbose=0)  # [[0.61519665 0.38480335]]
        index = np.argmax(prediction)
        output_store.predict_store[index] += 1

    def _get_prepared_image(self, image):

        # 224 x 224로 변환
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # 캠 보여주기
        # cv2.imshow("Webcam Image", image)

        # 이미지 -> numpy배열
        # input shape으로 변환
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # 노멀라이즈 (범위: -1 ~ 1)
        image = (image / 127.5) - 1

        return image

