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


def get_valid_records(data_path):
    files = glob.glob(data_path)
    X_files = []
    y_data = []
    data_json = [(json.loads(open(f, 'rb').read()), f) for f in files if ".json" in f][:50000]
    print(f'loading {len(data_json)} records.')
    for record, f in data_json:
        json_path = os.path.dirname(f)
        x_file = os.path.join(json_path, record["y_label_image_file"])
        y = record["y_label_points"]
        if os.path.exists(x_file):
            if len(y) == 4:
                X_files.append(x_file)
                y_data.append(y)
    assert (len(X_files) == len(y_data))
    return X_files, y_data


def load_data_tf(data_path: str):
    X_files, y_data = get_valid_records(data_path)

    y_data = np.array(y_data).reshape((len(y_data), 8))
    y_data = tf.data.Dataset.from_tensor_slices(y_data)

    for f in y_data.take(5):
        print(f.numpy())

    X_data = tf.data.Dataset.from_tensor_slices(X_files)
    for f in X_data.take(5):
        print(f.numpy())
    return X_data,y_data


def load_data(data_path: str):
    X_files, y_data = get_valid_records(data_path)

    out_y = np.array(y_data).reshape((len(y_data), 8))
    X_out = np.zeros((len(X_files), 256, 192, 3), dtype="uint8")
    for i, f in enumerate(X_files):
        # x = cv2.imread(f)
        # x = cv2.cvtColor(x, cv2.COLOR_RGB2BGR)
        X_out[i] = cv2.cvtColor(cv2.imread(f), cv2.COLOR_RGB2BGR)

    return X_out, out_y


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
    l_model.compile(loss="MAE", optimizer=tf.keras.optimizers.Adam(learning_rate=.0003))
    return l_model


def train_model(l_model, X, y):
    print(f"training on {len(X)} records.")
    l_model.fit(X, y, epochs=1000, batch_size=32)
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
        try:
            new_model.summary()
        except AttributeError as e:
            logging.warning(e)
        return new_model

    except OSError as e:
        logging.exception(
            f"no model was found for DTP phase 1, execute python {__file__} to auto generate a new model ")
        raise e


if __name__ == "__main__":
    data_dir_synthetic = join(dirname(__file__), "..", "models", "synthetic_data",
                              "synthetic_data_for_pipeline_transform",
                              "data", "*", "*")
    data_dir_real = join(dirname(__file__), "..", "data", "transcribed_stories",
                         "*", "*", "phase0", "*")
    model = None
    print("(O)verwrite, (R)esume training, (C)ancel, (T)est")
    yn = input()
    if "o" in yn.lower():
        print("okay.. creating..")
        data_dir_synthetic = join(dirname(__file__), "..", "models", "synthetic_data",
                                  "synthetic_data_for_pipeline_transform",
                                  "data", "*", "*")
        data_dir_real = join(dirname(__file__), "..", "data", "transcribed_stories",
                             "*", "*", "phase0", "*")

        model = create_model()

        X, y = load_data(data_dir_synthetic)
        model = train_model(model, X, y)

        X, y = load_data(data_dir_real)
        print(data_dir_real, len(X))
        model = train_model(model, X, y)

        model_file_name = data_dir = join(dirname(__file__), 'dtp_phase1_model.tf')
        model.save(model_file_name)

    if "r" in yn.lower():
        model = load_model()

        X, y = load_data(data_dir_synthetic)
        model = train_model(model, X, y)

        X, y = load_data(data_dir_real)
        print(data_dir_real, len(X))
        model = train_model(model, X, y)

        model_file_name = data_dir = join(dirname(__file__), 'dtp_phase1_model.tf')
        model.save(model_file_name)

    if "t" in yn[0].lower():
        load_data_tf(data_dir_synthetic)
else:
    model = None
    load_model()
