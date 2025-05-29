import keras
from keras import layers
import mlflow

from src.logger import get_logger
from src.custom_exceptions import CustomException

logger = get_logger(__name__)

class Classifier:
    def __init__(self,
                 dropout:float=0.5,
                 epsilon:float=1e-6,
                 lr:float=0.001,
                 weight_decay:float=0.0001,
                 beta_1:float=0.5,
                 beta_2:float=0.9
                 ):
        logger.info("Building Classifier Model")

        self.dropout = dropout
        self.epsilon = epsilon
        self.lr = lr
        self.decay = weight_decay
        self.b1 = beta_1
        self.b2 = beta_2
        
    def get_model(self, input_shape, num_classes) -> keras.Model:
        try:
            inputs = keras.Input(shape=input_shape)

            x = layers.Flatten()(inputs)

            x = layers.Dense(256, activation="relu")(x)
            x = layers.Dropout(self.dropout)(x)
            x = layers.BatchNormalization(epsilon=self.epsilon)(x)

            x = layers.Dense(128, activation="relu")(x)
            features = layers.Dropout(self.dropout)(x)

            logits = layers.Dense(num_classes)(features)

            model = keras.Model(inputs=inputs, outputs=logits)
            logger.info("Classifier Model Created Successfully")
            return model
        except CustomException as e:
            logger.error(f"Exception Raised When Creating Classifer Class: {str(e)}")
            raise CustomException("Exception Raised When Creating Classifer Class", e)

    def run_experiment(self,
                       train_ds,
                       test_ds, 
                       epochs,
                       input_shape, 
                       num_classes
                   ):
        try:
            with mlflow.start_run():
                mlflow.autolog()

                opt = keras.optimizers.AdamW(self.lr, self.decay, self.b1, self.b2)
                classifier = self.get_model(input_shape, num_classes)

                classifier.compile(optimizer=opt,
                            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                            metrics=[keras.metrics.SparseCategoricalAccuracy()])
                logger.info("Model Compiled Successfully")

                early_stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, mode="min")
                lron = keras.callbacks.ReduceLROnPlateau(monitor="val_loss", patience=5, mode="min")
                
                logger.info("Starting Training Experiment")
                history = classifier.fit(train_ds,
                                         epochs=epochs,
                                         validation_data=test_ds,
                                         callbacks=[early_stop, lron])
                
                logger.info("Experiment Complete")
                return history
        except CustomException as e:
            logger.error(f"Exception Raised When Running Training Experiment: {str(e)}") 