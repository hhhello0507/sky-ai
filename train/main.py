# General imports
import os
from pathlib import Path

import numpy as np
from anomalib.deploy import OpenVINOInferencer
from anomalib.data.task_type import TaskType
from anomalib.post_processing import ImageResult
from matplotlib import pyplot as plt
from anomalib.post_processing import Visualizer, VisualizationMode
from PIL import Image

openvino_model_path = Path.cwd() / "weights" / "openvino" / "model.bin"
metadata_path = Path.cwd() / "weights" / "openvino" / "metadata.json"
print(openvino_model_path.exists(), metadata_path.exists())

inferencer = OpenVINOInferencer(
    path=openvino_model_path,  # Path to the OpenVINO IR model.
    metadata=metadata_path,  # Path to the metadata file.
    device="CPU",  # We would like to run it on an Intel CPU.
)



def visualize(title: str, task: TaskType, predictions: ImageResult):
    visualizer = Visualizer(mode=VisualizationMode.FULL, task=task)
    output_image = visualizer.visualize_image(predictions)
    img = Image.fromarray(output_image)

    plt.figure(dpi=300)
    plt.imshow(img)
    plt.title(title)


def predict(predict_image: np.ndarray, index: int, show: bool = True):
    predictions = inferencer.predict(image=predict_image)

    print(predictions.pred_score, predictions.pred_label)

    if show:
        visualize(title=f'classification - {index} {predictions.pred_label}', task=TaskType.CLASSIFICATION,
                  predictions=predictions)
        # visualize(title=f'segmentation - {index} {predictions.pred_label}', task=TaskType.SEGMENTATION)
        plt.show()


def main():
    print('load')

    # for i in range(30):
    #     abnormal_path = f'abnormal_{i}.jpg'
    #     image_path = f"./{product_name}/abnormal/{abnormal_path}"
    #     image: np.ndarray = read_image(path=image_path)
    #     # print(image.shape)
    #     predict(predict_image=image, index=i)

    # for i in range(30):
    #     abnormal_path = f'normal_{i}.jpg'
    #     image_path = f"./{product_name}/normal/{abnormal_path}"
    #     image: np.ndarray = read_image(path=image_path)
    #     # print(image.shape)
    #     predict(predict_image=image, index=i)


if __name__ == '__main__':
    main()
