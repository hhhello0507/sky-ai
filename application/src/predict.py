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

from src.local import model_folder_path


def predictImage(model_name: str, predict_image: np.ndarray):
    openvino_model_path = Path(model_folder_path) / model_name / "weights" / "openvino" / "model.bin"
    metadata_path = Path(model_folder_path) / model_name / "weights" / "openvino" / "metadata.json"

    if not openvino_model_path.exists() or not metadata_path.exists():
        raise Exception("model is not exist")

    inferencer = OpenVINOInferencer(
        path=openvino_model_path,  # Path to the OpenVINO IR model.
        metadata=metadata_path,  # Path to the metadata file.
        device="CPU",  # We would like to run it on an Intel CPU.
    )

    predictions = inferencer.predict(image=predict_image)

    result = (predictions.pred_score, predictions.pred_label)
    print(result)
    return result

    # if show:
    #     visualize(title=f'classification - {index} {predictions.pred_label}', task=TaskType.CLASSIFICATION,
    #               predictions=predictions)
    #     # visualize(title=f'segmentation - {index} {predictions.pred_label}', task=TaskType.SEGMENTATION)
    #     plt.show()

# def visualize(title: str, task: TaskType, predictions: ImageResult):
#     visualizer = Visualizer(mode=VisualizationMode.FULL, task=task)
#     output_image = visualizer.visualize_image(predictions)
#     img = Image.fromarray(output_image)
#
#     plt.figure(dpi=300)
#     plt.imshow(img)
#     plt.title(title)
