from keras.models import load_model
import cv2
import numpy as np
import serial
from datetime import datetime, timedelta
import asyncio

np.set_printoptions(suppress=True)
model = load_model("g_model.h5", compile=False)
print("load model")
class_names = open("labels.txt", "r").readlines()
camera = cv2.VideoCapture(1)

py_serial = serial.Serial(
    port="COM3",
    baudrate=9600,
)

d = [0 for _ in range(len(class_names))]


async def predict():
    global d
    while True:
        # 촬영
        _, image = camera.read()

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
        prediction = model.predict(image, verbose=0)  # [[0.61519665 0.38480335]]
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # 예측 결과, 점수 출력
        print(f"결과: {class_name.split()[1]}   ", end="")
        print(f"점수: {np.round(confidence_score * 100)}%")

        d[index] += 1
        print(d)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        await asyncio.sleep(0.01)


async def sendArduino():
    global d
    before_time = datetime.now()
    while True:
        current_time = datetime.now()
        if before_time + timedelta(seconds=1) < current_time:
            mxIdx = [*sorted([i for i in enumerate(d)], key=lambda x: x[1])][0][0]
            print(f"sended - mxIdx: {mxIdx}, encoded: {str(mxIdx).encode()}")
            py_serial.write(str(mxIdx).encode())

            before_time = current_time
            d = [0 for _ in range(len(class_names))]
        await asyncio.sleep(0.01)


async def main():
    await asyncio.gather(predict(), sendArduino())


if __name__ == "__main__":
    asyncio.run(main())

    camera.release()
    cv2.destroyAllWindows()
