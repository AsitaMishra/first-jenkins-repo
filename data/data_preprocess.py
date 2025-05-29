import keras
import tensorflow as tf

from src.custom_exceptions import CustomException
from src.logger import get_logger

logger = get_logger(__name__)

class DataProc:
    def __init__(self,
                shuffle_buffer:int = 3,
                repeat_count:int = 2,
                batch_size:int = 32,
                autotune: any = tf.data.AUTOTUNE):
        self.SHUFFLE_BUFFER = shuffle_buffer
        self.REPEAT_CNT = repeat_count
        self.BATCH_SIZE = batch_size
        self.AUTOTUNE = autotune

        self.data_aug = keras.Sequential([
                            keras.layers.RandomFlip("horizontal"),
                            keras.layers.RandomRotation(0.1)
                        ])

        logger.info(f"Preparing For Data Processing")

    def __cast(self, images, labels):
        images = tf.cast(images, dtype=tf.float32)
        images = images/255.0

        labels = tf.cast(labels, dtype=tf.float32)

        return images, labels
    
    @tf.autograph.experimental.do_not_convert
    def __map(self, ds):
        try: 
            ds = ds.map(lambda x, y: (self.__cast(x, y)),
                        num_parallel_calls=self.AUTOTUNE)
            # ds = ds.map(lambda x, y: (self.data_aug(x), y),
            #             num_parallel_calls=self.AUTOTUNE)
            ds = ds.shuffle(self.SHUFFLE_BUFFER)
            # ds = ds.repeat(self.REPEAT_CNT)
            ds = ds.batch(self.BATCH_SIZE, 
                        num_parallel_calls=self.AUTOTUNE)
            
            return ds
        except Exception as e:
            logger.error("Failed To Map Datasets")
            raise CustomException("Failed To Map Datasets", e)
    
    def __load_data(self, train_ds, test_ds):
        try:
            train_ds = tf.data.Dataset.from_tensor_slices(train_ds)
            test_ds = tf.data.Dataset.from_tensor_slices(test_ds)

            logger.info("Data Successfully Loaded For Preprocessing")

            return train_ds, test_ds
        except Exception as e:
            logger.error("Failed To Load Data As Datasets")
            raise CustomException("Failed To Load Data As Datasets", e)

    def __call__(self, train_ds, test_ds):
        try:
            logger.info("Loading Data For Preprocessing")
            train_ds, test_ds = self.__load_data(train_ds, test_ds)
            logger.info("Mapping Datasets")
            train_ds = self.__map(train_ds)
            test_ds = self.__map(test_ds)

            logger.info("Preprocessing Successful")
            return train_ds, test_ds
        except CustomException as e:
            logger.error(f"Exception When Calling Data Preprocess Class: {str(e)}")