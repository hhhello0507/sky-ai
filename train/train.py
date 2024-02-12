import os

from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint

from anomalib.data.folder import Folder
from anomalib.data.task_type import TaskType
from anomalib.models import Padim
from anomalib.post_processing import NormalizationMethod, ThresholdMethod
from anomalib.utils.callbacks import (
    MetricsConfigurationCallback,
    MinMaxNormalizationCallback,
    PostProcessingConfigurationCallback,
)
from anomalib.utils.callbacks.export import ExportCallback, ExportMode

from constant import app_title

def train(product_name, train_path) -> str:

    datamodule = Folder(
        root=train_path,
        normal_dir="normal",
        abnormal_dir="abnormal",
        normal_split_ratio=0.2,
        image_size=(640, 480),
        train_batch_size=32,
        eval_batch_size=32,
        task=TaskType.CLASSIFICATION,
    )
    datamodule.setup()  # Split the data to train/val/test/prediction sets.
    datamodule.prepare_data()  # Create train/val/test/predict dataloaders

    model = Padim(
        input_size=(640, 480),
        backbone="resnet18",
        layers=["layer1", "layer2", "layer3"],
    )

    export_path = str(os.path.join(app_title, product_name))

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
            dirpath=export_path,
            filename=f"{product_name}_model",
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

    return export_path
