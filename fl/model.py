# create model.py for training a lightweight model
# need to use mobilenet - lightweight and very fast
# efficient training is also possible with this.

import tensorflow as tf
import numpy as np
import cv2
import os

classes = ["normal", "abnormal"]

class_labels = {classes: i for i, classes in enumerate(classes)}
number_of_classes = 2

# greater image_size => more data goes to model but processing time increases.
IMAGE_SIZE = (160, 160)

federatedLearningcounts = 4
local_client_epochs = 10
local_client_batch_size = 8

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(160, 160, 3),
    alpha=1.0,
    include_top=False,
    weights="imagenet",
    input_tensor=None,
    pooling=None,
    classes=2,
    classifier_activation="softmax"
)

