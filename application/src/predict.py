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


# def visualize(title: str, task: TaskType, predictions: ImageResult):
#     visualizer = Visualizer(mode=VisualizationMode.FULL, task=task)
#     output_image = visualizer.visualize_image(predictions)
#     img = Image.fromarray(output_image)
#
#     plt.figure(dpi=300)
#     plt.imshow(img)
#     plt.title(title)


def predict(predict_image: np.ndarray):
    openvino_model_path = Path.cwd() / "weights" / "openvino" / "model.bin"
    metadata_path = Path.cwd() / "weights" / "openvino" / "metadata.json"

    if not openvino_model_path.exists() or not metadata_path.exists():
        raise Exception("model is not exist")

    inferencer = OpenVINOInferencer(
        path=openvino_model_path,  # Path to the OpenVINO IR model.
        metadata=metadata_path,  # Path to the metadata file.
        device="CPU",  # We would like to run it on an Intel CPU.
    )

    predictions = inferencer.predict(image=predict_image)

    print(predictions.pred_score, predictions.pred_label)

    # if show:
    #     visualize(title=f'classification - {index} {predictions.pred_label}', task=TaskType.CLASSIFICATION,
    #               predictions=predictions)
    #     # visualize(title=f'segmentation - {index} {predictions.pred_label}', task=TaskType.SEGMENTATION)
    #     plt.show()

