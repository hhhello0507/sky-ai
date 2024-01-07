import cv2
import numpy as np
from keras.models import load_model

from src.model.store import Store


class SkyAI:

    def __init__(self, model_path):
        self.model = load_model(model_path, compile=False)

    def predict(self, image, output_store: Store):

        # 224 x 224로 변환
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # 캠 보여주기
        cv2.imshow("Webcam Image", image)

        # 이미지 -> numpy배열
        # input shape으로 변환
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # 노멀라이즈 (범위: -1 ~ 1)
        image = (image / 127.5) - 1

        # 예측
        prediction = self.model.predict(image, verbose=0)  # [[0.61519665 0.38480335]]
        index = np.argmax(prediction)
        # class_name = class_names[index]
        # confidence_score = prediction[0][index]
        #
        # # 예측 결과, 점수 출력
        # print(f"결과: {class_name.split()[1]}   ", end="")
        # print(f"점수: {np.round(confidence_score * 100)}%")
        output_store.predict_store[index] += 1

