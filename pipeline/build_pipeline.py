import os

import keras
import keras.backend as K
import numpy as np
import tensorflow as tf

from data.data_preprocess import DataProc
from model.classifier import Classifier

from src.logger import get_logger
from src.custom_exceptions import CustomException

import gc

logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        gc.enable()

        os.environ["KERAS_BACKEND"] = "tensorflow"
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        if tf.config.list_physical_devices('GPU'):
            logger.info("GPU Detected")

        train_ds, test_ds = keras.datasets.cifar10.load_data()

        img_shape = train_ds[0].shape[1:]
        num_classes = len(np.unique(train_ds[1]))

        logger.info("Building Pipeline")
        dproc = DataProc()
        train_ds, test_ds = dproc(train_ds, test_ds)

        K.clear_session()
        classifier = Classifier()
        hist = classifier.run_experiment(train_ds,
                                         test_ds, 
                                         epochs=1, 
                                         input_shape=img_shape, 
                                         num_classes=num_classes)
        
        gc.collect()
        gc.disable()
    except CustomException as e:
        logger.error(f"Exception Raised When Building Pipeline: {str(e)}")
        raise CustomException("Exception Raised When Building Pipeline", e)