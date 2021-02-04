import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from keras.utils.vis_utils import plot_model
from skimage import io
from matplotlib import pyplot
import os


#load the model
base_model = keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
#freeze base model
base_model.trainable = False
#summarize the model
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.Flatten(),
    # tf.keras.layers.Conv2D(32,kernel_size=3, activation = 'relu'), -
    # tf.keras.layers.MaxPooling2D(pool_size=(2,2)), -
    # tf.keras.layers.Dropout(0.6), -
    # tf.keras.layers.BatchNormalization(), -
    # tf.keras.layers.Dense(256, activation='relu'), -
    # tf.keras.layers.Dropout(0.6), - 
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.6),  
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(32, activation='relu'),
    # tf.keras.layers.Dropout(0.2), -
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(16, activation='relu'),
    # tf.keras.layers.Dropout(0.1), -
    # tf.keras.layers.Flatten(), -
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(5, activation='softmax')
])

# plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
# 


model.compile(
    optimizer='adam',  #can also try to use rmsprop/adam/sgd otimizer
    # it seems that rmsprop performs better than adam on a more consisent basis
    loss = 'sparse_categorical_crossentropy', # will also try sparse_categorical_crossentropy/categorical_crossentropy
    metrics=['accuracy'] # will also try to interchange with 'sparse_categorical_accuracy'
)

model.summary()

# Quick save of our file paths for the data directorys 
Train = r'Image_scoring\Data\Training'
Vali = r'Image_scoring\Data\Validation'


# we will create a data augmentor that will augment our images before seeing the
# model and without having to save locally 
datagen = ImageDataGenerator(
    rotation_range = 45, #rotates image between 0 and 45 degrees
    width_shift_range = .2, # the % percent change in the width
    height_shift_range = .2,
    shear_range = .2, # how much of a percent we will shear the image
    zoom_range = .2, #what percent we want to zoom in on each image
    horizontal_flip = True,
    fill_mode = 'constant', #other options to try are nearest,constant,reflect,wrapped
    cval = 125
)
# Create a training datagenerator that will be used to pass into the call to the
# directory so we dont need to save these pictures locally
train_datagen = ImageDataGenerator(
        rescale=1./255,
        width_shift_range = .2,
        height_shift_range = .2,
        rotation_range=45,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode = 'constant',
        cval = 125)

# Doing the same thing above for the validation set but we dont need to do much
# other than rescale it
validation_datagen = ImageDataGenerator(rescale=1./255)

# after we create the train data generator we can use that to pass into the directory
# flow this is where we will actually generate our augmented images
train_generator = train_datagen.flow_from_directory(
        Train,  # this is the input directory
        target_size=(224, 224),  # all images will be resized 
        color_mode = 'rgb',
        batch_size=32, # each epoch of training will see ~1200/16 which is 100 iterations and in each iteration it sees 16 images, Original int was 32 will try 25
        class_mode='sparse', # will need to change between "categorical" and "sparse" depending on loss function of model.compile
        shuffle=True,
        seed = 42,
        # subset = "training",
        interpolation="bilinear",
        follow_links=False,
        )
# the validation generator will be similar in style to the train generator
validation_generator = validation_datagen.flow_from_directory(
        Vali,  
        target_size=(224, 224), 
        color_mode = 'rgb',
        batch_size=32, 
        class_mode='sparse',  # will need to change between categorical and sparse depending on loss function of model.compile
        shuffle=True,
        seed = 42,
        # subset = "validation",
        interpolation="bilinear",
        follow_links=False,
)

# Callbacks to use for the model.fit
# ES will stop if loss metric hasnt increased in 10 epochs
earlyStopping = EarlyStopping(monitor='accuracy', patience=75, verbose=1, mode='auto')
# MC will monitor for metric accuracy and save only if metric accuracy improves
mcp_save = ModelCheckpoint('.mdl_wts.hdf5', save_best_only=True, monitor='accuracy', mode='auto')
# RLROP will reduce learning rate once learning stagnates
reduce_lr_loss = ReduceLROnPlateau(monitor='accuracy', factor=0.1, patience=75, verbose=1, mode='auto')


# Fitting the model
# Found that epoch 7 and 14 are performing well when using adam as optimizer
model1 = model.fit(
        train_generator,
        steps_per_epoch=int(len(train_generator)/32), # 1160 // 15,    #The 2 slashes division return rounded integer, the 32 is batch size
        epochs=120, #can play with epochs, will go much higher and let it run until it finds best fit and auto save it in callbacks
        validation_data=validation_generator,
        validation_steps=int(len(train_generator)/32), # 800 // 15, train_generator
        callbacks=[earlyStopping, mcp_save, reduce_lr_loss]
)
model.save('img_clustering_augmented_model.h5')  # always save your weights after training or during training

# plot learning curves
pyplot.title('Learning Curves')
pyplot.xlabel('Epoch')
pyplot.ylabel('Accuracy')
pyplot.plot(model1.history['accuracy'], label='accuracy')
pyplot.plot(model1.history['val_accuracy'], label='val_accuracy')
pyplot.legend()
pyplot.show()