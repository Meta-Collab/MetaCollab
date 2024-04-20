#reference - https://github.com/adap/flower/tree/main/examples/advanced-tensorflow

from typing import Dict, Optional, Tuple
import flwr as fl

import tensorflow as tf
import os
import cv2
import numpy as np
from sklearn.utils import shuffle
from keras.preprocessing import image

server_address = "0.0.0.0:5050"

classes = ["normal", "abnormal"]
class_labels = {classes: i for i, classes in enumerate(classes)}
number_of_classes = 2

# greater image_size => more data goes to model but processing time increases.
IMAGE_SIZE = (160, 160)

federatedLearningcounts = 4
local_client_epochs = 10
local_client_batch_size = 8

def main() -> None:
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
    # freeze the layers in the base model - they don't get updated
    base_model.trainable = False

    x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    outputs = tf.keras.layers.Dense(2, activation='softmax')(x)

    model = tf.keras.Model(inputs=base_model.input, outputs=outputs)

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    strategy = fl.server.strategy.FedAvg(
        fraction_fit=0.3,
        fraction_evaluate=0.2,
        min_fit_clients=2,
        min_evaluate_clients=2,
        min_available_clients=2,
        evaluate_fn=get_evaluate_fn(model),
        on_fit_config_fn=fit_config,
        on_evaluate_config_fn=evaluate_config,
        initial_parameters=fl.common.ndarrays_to_parameters(
            model.get_weights()),
    )

    fl.server.start_server(
        server_address=server_address,
        config=fl.server.ServerConfig(num_rounds=federatedLearningcounts),
        strategy=strategy
    )

def load_dataset():
    # defining the directory with the server's test images. We only use the test images!
    directory = "datasets/ds_server"
    sub_directories = ["test", "train"]

    loaded_dataset = []
    for sub_directory in sub_directories:
        path = os.path.join(directory, sub_directory)
        images = []
        labels = []

        print("Server dataset loading {}".format(sub_directory))

        for folder in os.listdir(path):
            label = class_labels[folder]
            # print(label)

            for file in os.listdir(os.path.join(path,folder)):
                img_path = os.path.join(os.path.join(path, folder), file)

                image = cv2.imread(img_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, IMAGE_SIZE)

                images.append(image)
                labels.append(label)

        images = np.array(images, dtype= 'float32')
        labels = np.array(labels, dtype= 'int32')

        loaded_dataset.append((images, labels))
    
    return loaded_dataset

def get_evaluate_fn(model):
    (training_images, training_labels), (test_images, test_labels) = load_dataset()
    print("[Server] test_images shape:", test_images.shape)
    print("[Server] test_labels shape:", test_labels.shape)

    weights = model.get_weights()
    print(type(weights))

    with open('gfg.txt', 'w+') as f:
         for items in weights:
             f.write('%s\n' %items)
     
    print("File written successfully")    
    # close the file
    f.close()

    def evaluate(
        server_round: int,
        parameters: fl.common.NDArrays,
        config: Dict[str, fl.common.Scalar],
    ) -> Optional[Tuple[float, Dict[str, fl.common.Scalar]]]:
        print("======= server round %s/%s evaluate() ===== " %(server_round, federatedLearningcounts))

        print("parameters:\n")
        print(type(parameters))

        model.set_weights(parameters)
        loss, accuracy = model.evaluate(test_images, test_labels, verbose=0)
        print("======= server round %s/%s accuracy : %s =======" %(server_round, federatedLearningcounts,accuracy))

        if (server_round == federatedLearningcounts):
            print("Saving updated model locally..")
            # model.save('saved_models/mobilenetv2.h5')  # save model in .h5 format
            model.export('saved_models/mobilenetv2')      # save model in SavedModel format - .pb format

            # test the updated model
            test_updated_model(model)

        return loss, {"accuracy": accuracy}
    return evaluate

def fit_config(server_round: int):
    config = {
        "batch_size": local_client_batch_size,
        "local_epochs": local_client_epochs,
    }
    return config

def evaluate_config(server_round: int):
    val_steps = 4
    return {"val_steps": val_steps}

def process_image(file):
    test_image = cv2.imread(file)
    test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
    test_image = cv2.resize(test_image, IMAGE_SIZE)
    return test_image

def test_updated_model(model):
    test_image = process_image("datasets/test.jpg")

    print("Testing the final model on an image...")
    image_test_result = model.predict(np.expand_dims(test_image, axis=0))
    print(image_test_result[0])

    highest_prediction_score = max(image_test_result[0])
    highest_prediction_score_index = 0
    for i in range(len(image_test_result[0])):
        if image_test_result[0][i] == highest_prediction_score:
            highest_prediction_score_index = i

    most_confident_class = classes[highest_prediction_score_index]
    print("The model mostly predicted %s with a score/confidence of %s" %(most_confident_class, highest_prediction_score))

if __name__ == "__main__":
    main()