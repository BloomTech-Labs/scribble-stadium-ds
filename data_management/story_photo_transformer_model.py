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
import matplotlib.pyplot as plt


import joblib


def load_data(dir):
    path_real = dir
    real_set=glob.glob(path_real)

    X_real =np.array([ cv2.cvtColor(cv2.imread(x),cv2.COLOR_RGB2BGR) for x in real_set if "X_input" in x ])
    y_real =[ json.loads(open(y,'rb').read() )["y_label_points"] for y in real_set if ".json" in y ]
    y_real = np.array(y_real).reshape((X_real.shape[0],8))
    return (X_real, y_real)
    print(dir)
    print(y_real)

  

def create_model():
        
    img_inputs = keras.Input(shape=(256, 256-64, 3))
    x=img_inputs
    
    x = layers.Flatten()(x)

    x = layers.Dense(64, activation="relu")(x)
    x = layers.Dense(64, activation="relu")(x)
    x = layers.Dense(64, activation="relu")(x)
    x = layers.Dense(32, activation="relu")(x)
    x = layers.Dense(24, activation="relu")(x)
    x = layers.Dense(16, activation="relu")(x)
    outputs = layers.Dense(8,)(x)
    
    model = keras.Model(inputs=img_inputs, outputs=outputs, name="FC_Model")
    return model

def train_model(dir, model):
    examples = glob.glob(dir)
    records = {join(dirname(fn),basename(fn).split(".")[0]) for fn in examples}
    X_train =[ cv2.cvtColor(cv2.imread(x),cv2.COLOR_RGB2BGR) for x in examples if "X_input" in x ]
    y_train =[ json.loads( open(y,'rb').read() )["y_label_points"] for y in examples if ".json" in y ]
    X_train = np.array(X_train)
    y_train = np.array(y_train).reshape((X_train.shape[0],8))
    model.compile(loss="MAE",optimizer=tf.keras.optimizers.Adam(learning_rate=.0001))
    model.fit(X_train,y_train)
    model.save('dtp_phase1_model.tf', save_format="tf")
    return model

def predict_pts(X_input : np.array) -> list:
    assert len(X_input.shape) == 3
    X_input = np.expand_dims(X_input, axis = 0) # to add a bacth diminsion
    pred =  model.predict(X_input)
    return pred.reshape(4,2).tolist()


if __name__ == "__main__":

    data_dir = join(dirname(__file__),"..","models","synthetic_data","synthetic_data_for_pipeline_transform","data","*","*")
    X_real, y_real = load_data(data_dir)  
    model = train_model(data_dir, create_model())

'''
for loading the model)
'''
# new_model = tf.keras.models.load_model('dtp_phase1_model.tf')
# new_model.summary()
# print(predict_pts(X_real[0]))##


