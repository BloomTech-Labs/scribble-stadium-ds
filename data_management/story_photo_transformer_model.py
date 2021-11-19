import os
os.add_dll_directory(r'e:\cuda\bin')
import logging

import cv2
import glob
from os.path import relpath
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
import json

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def load_data(path: str):
    files = glob.glob(path)

    lX = np.array([cv2.cvtColor(cv2.imread(x), cv2.COLOR_RGB2BGR) for x in files if "X_input" in x])
    ly = [json.loads(open(y, 'rb').read())["y_label_points"] for y in files if ".json" in y]
    ly = np.array(ly).reshape((lX.shape[0], 8))
    return lX, ly


def create_model():
    img_inputs = keras.Input(shape=(256, 256 - 64, 3))
    x = img_inputs

    x = layers.Flatten()(x)

    x = layers.Dense(32, activation="relu")(x)
    x = layers.Dense(64, activation="relu")(x)
    x = layers.Dense(64, activation="relu")(x)
    x = layers.Dense(32, activation="relu")(x)
    x = layers.Dense(24, activation="relu")(x)
    x = layers.Dense(16, activation="relu")(x)
    outputs = layers.Dense(8, )(x)

    l_model = keras.Model(inputs=img_inputs, outputs=outputs, name="FC_Model")
    l_model.compile(loss="MAE", optimizer=tf.keras.optimizers.Adam(learning_rate=.0001))
    return l_model


def train_model(l_model, X, y):
    l_model.fit(X, y, epochs=1000, batch_size=16)
    l_model.save('dtp_phase1_model.tf', save_format="tf")
    return l_model


def predict_pts(x: np.array) -> list:
    assert len(x.shape) == 3
    x = np.expand_dims(x, axis=0)  # to add a bacth diminsion
    pred = model.predict(x)
    return pred.reshape(4, 2).tolist()


def load_model():
    try:
        global model
        model_file_name = data_dir = join(dirname(__file__), 'dtp_phase1_model.tf')
        new_model = tf.keras.models.load_model(model_file_name)
        print("loaded existing model")
        new_model.summary()
        model = new_model

    except OSError as e:
        logging.exception(
            f"no model was found for DTP phase 1, execute python {__file__} to auto generate a new model ")
        raise e


if __name__ == "__main__":
    model = None
    print("(O)verwrite, (R)esume training, (C)ancel")
    yn = input()
    if "o" in yn.lower():
        print("okay.. creating..")
        data_dir_synthetic = join(dirname(__file__), "..", "models", "synthetic_data",
                                  "synthetic_data_for_pipeline_transform",
                                  "data", "*", "*")
        data_dir_real = join(dirname(__file__), "..", "data", "transcribed_stories",
                             "*","*","phase0", "*")

        model = create_model()

        X, y = load_data(data_dir_synthetic)
        model = train_model(model, X, y)

        X, y = load_data(data_dir_real)
        print(data_dir_real,len(X))
        model = train_model(model, X, y)


        model_file_name = data_dir = join(dirname(__file__), 'dtp_phase1_model.tf')
        model.save(model_file_name)

    if "r" in yn.lower():
        model=None
        load_model()
        data_dir_synthetic = join(dirname(__file__), "..", "models", "synthetic_data",
                                  "synthetic_data_for_pipeline_transform",
                                  "data", "*", "*")
        data_dir_real = join(dirname(__file__), "..", "data", "transcribed_stories",
                             "*", "*", "phase0", "*")

        X, y = load_data(data_dir_synthetic)
        model = train_model(model, X, y)

        X, y = load_data(data_dir_real)
        print(data_dir_real, len(X))
        model = train_model(model, X, y)

        model_file_name = data_dir = join(dirname(__file__), 'dtp_phase1_model.tf')
        model.save(model_file_name)
else:
    model = None
    load_model()
