# General imports
import os
from pathlib import Path

import numpy as np
from anomalib.data.utils import read_image
from anomalib.deploy import OpenVINOInferencer
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint

# For downloading dataset and robot api
from anomalib.data.utils import DownloadInfo, download_and_extract

# For preparing your own dataset
from anomalib.data.folder import Folder
from anomalib.data.task_type import TaskType

# For preparing your model
from anomalib.models import Padim

# For preparing callbacks
from anomalib.post_processing import NormalizationMethod, ThresholdMethod
from anomalib.utils.callbacks import (
    MetricsConfigurationCallback,
    MinMaxNormalizationCallback,
    PostProcessingConfigurationCallback,
)
from anomalib.utils.callbacks.export import ExportCallback, ExportMode

# For visualization in the notebook
from matplotlib import pyplot as plt
from anomalib.post_processing import Visualizer, VisualizationMode
from PIL import Image


def main():
    print('load')
    product_name = 'data1'

    def training():
        path = os.getcwd() + f"\\{product_name}"

        datamodule = Folder(
            root=path,
            normal_dir="normal",
            abnormal_dir="abnormal",
            normal_split_ratio=0.2,
            image_size=(640, 480),
            train_batch_size=32,
            eval_batch_size=32,
            task=TaskType.CLASSIFICATION,
        )
        datamodule.setup()  # Split the data to train/val/test/prediction sets.
        print('set upped')
        datamodule.prepare_data()  # Create train/val/test/predict dataloaders

        i, data = next(enumerate(datamodule.val_dataloader()))
        print(data.keys())

        model = Padim(
            input_size=(640, 480),
            backbone="resnet18",
            layers=["layer1", "layer2", "layer3"],
        )

        callbacks = [
            MetricsConfigurationCallback(
                task=TaskType.CLASSIFICATION,
                image_metrics=["AUROC"],
            ),
            ModelCheckpoint(
                mode="max",
                monitor="image_AUROC",
            ),
            PostProcessingConfigurationCallback(
                normalization_method=NormalizationMethod.MIN_MAX,
                threshold_method=ThresholdMethod.ADAPTIVE,
            ),
            MinMaxNormalizationCallback(),
            ExportCallback(
                input_size=(640, 480),
                dirpath=str(Path.cwd()),
                filename="model",
                export_mode=ExportMode.OPENVINO,
            ),
        ]

        trainer = Trainer(
            callbacks=callbacks,
            accelerator="auto",
            auto_scale_batch_size=False,
            check_val_every_n_epoch=1,
            devices=1,
            gpus=None,
            max_epochs=1,
            num_sanity_val_steps=0,
            val_check_interval=1.0,
        )
        trainer.fit(model=model, datamodule=datamodule)

    # training()


    openvino_model_path = Path.cwd() / "weights" / "openvino" / "model.bin"
    metadata_path = Path.cwd() / "weights" / "openvino" / "metadata.json"
    print(openvino_model_path.exists(), metadata_path.exists())

    inferencer = OpenVINOInferencer(
        path=openvino_model_path,  # Path to the OpenVINO IR model.
        metadata=metadata_path,  # Path to the metadata file.
        device="CPU",  # We would like to run it on an Intel CPU.
    )

    def predict(predict_image: np.ndarray, index: int, show: bool=True):
        predictions = inferencer.predict(image=predict_image)

        print(predictions.pred_score, predictions.pred_label)

        def visualize(title: str, task: TaskType):
            visualizer = Visualizer(mode=VisualizationMode.FULL, task=task)
            output_image = visualizer.visualize_image(predictions)
            img = Image.fromarray(output_image)

            plt.figure(dpi=300)
            plt.imshow(img)
            plt.title(title)
        if show:
            visualize(title=f'classification - {index} {predictions.pred_label}', task=TaskType.CLASSIFICATION)
            # visualize(title=f'segmentation - {index} {predictions.pred_label}', task=TaskType.SEGMENTATION)
            plt.show()

    # for i in range(30):
    #     abnormal_path = f'abnormal_{i}.jpg'
    #     image_path = f"./{product_name}/abnormal/{abnormal_path}"
    #     image: np.ndarray = read_image(path=image_path)
    #     # print(image.shape)
    #     predict(predict_image=image, index=i)

    for i in range(30):
        abnormal_path = f'normal_{i}.jpg'
        image_path = f"./{product_name}/normal/{abnormal_path}"
        image: np.ndarray = read_image(path=image_path)
        # print(image.shape)
        predict(predict_image=image, index=i)

if __name__ == '__main__':
    main()
