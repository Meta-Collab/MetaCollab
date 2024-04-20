text = """In the era of big data and machine learning, the demand for efficient, privacy-preserving, and scalable methods of training models on decentralized data has become increasingly critical. Federated Learning (FL) has emerged as a groundbreaking approach to address these challenges by enabling model training across distributed devices or servers without centralized data aggregation. This essay delves into the intricacies of federated learning, exploring its principles, applications, challenges, and future prospects.
Principles of Federated Learning
Federated Learning operates on the principle of decentralized model training, where instead of pooling all data in a central server, model training occurs locally on individual devices or servers. The process involves multiple rounds of communication between the central server and the participating devices. These rounds typically consist of three main steps: selection, training, and aggregation.
Selection: In the selection phase, devices or servers are chosen to participate in the training process. This can be based on various criteria such as device availability, data quality, or computational resources.
Training: Selected devices perform local training using their respective data while keeping the model parameters private. Each device computes updates to the model based on its local data and sends these updates to the central server.
Aggregation: The central server aggregates the model updates received from participating devices to create a global model. This aggregated model is then sent back to the devices, and the process iterates over multiple rounds to refine the global model.
The key advantage of federated learning lies in its ability to train models without the need to centralize sensitive data, thereby preserving user privacy and reducing communication overhead.
Applications of Federated Learning
Federated Learning finds applications across various domains where data privacy, scalability, and real-time learning are crucial. Some notable applications include:
Healthcare: In healthcare, federated learning enables collaborative model training across hospitals or medical institutions without sharing sensitive patient data. Models trained using FL can be used for disease diagnosis, personalized treatment recommendations, and drug discovery.
Internet of Things (IoT): With the proliferation of IoT devices, federated learning offers a solution for training models directly on edge devices. This enables applications such as predictive maintenance, anomaly detection, and smart home automation while preserving user privacy.
Finance: In the finance sector, federated learning can be applied to fraud detection, risk assessment, and customer segmentation while complying with stringent data privacy regulations such as GDPR and CCPA.
Telecommunications: Federated learning can optimize network performance, predict user behavior, and improve quality of service in telecommunications networks without compromising user privacy.
Challenges and Limitations
Despite its promises, federated learning faces several challenges and limitations that need to be addressed for widespread adoption:
Heterogeneity: Devices participating in federated learning may have diverse computational capabilities, network conditions, and data distributions, leading to challenges in model aggregation and convergence.
Communication Overhead: Federated learning requires frequent communication between the central server and participating devices, leading to increased communication overhead, especially in bandwidth-limited environments.
Privacy and Security: While federated learning aims to preserve privacy, there are still concerns regarding the leakage of sensitive information through model updates or inference attacks.
Bias and Fairness: Biases present in local datasets can propagate to the global model, leading to fairness issues and inaccurate predictions, especially in applications such as healthcare and finance.
Future Directions
Addressing the challenges of federated learning requires further research and innovation. Some promising directions for the future development of federated learning include:
Federated Optimization Algorithms: Developing efficient and robust optimization algorithms tailored for federated learning scenarios to handle heterogeneity and non-IID (non-identically distributed) data.
Privacy-Preserving Techniques: Advancing privacy-preserving techniques such as differential privacy, secure multi-party computation, and homomorphic encryption to enhance the security and privacy guarantees of federated learning.
Model Personalization: Exploring techniques for personalized federated learning to adapt models to individual user preferences and characteristics while maintaining privacy.
Fairness and Bias Mitigation: Integrating fairness-aware techniques into federated learning algorithms to mitigate biases and ensure fairness in model predictions across diverse user populations.
Edge Computing Integration: Leveraging edge computing infrastructure to perform local model training and inference on edge devices, reducing communication overhead and improving real-time learning capabilities.
Conclusion
Federated Learning represents a paradigm shift in machine learning, enabling collaborative model training across distributed data sources while preserving privacy and scalability. Its applications span across various domains, from healthcare to finance to IoT. However, challenges such as heterogeneity, communication overhead, and privacy concerns must be addressed for federated learning to reach its full potential. Continued research and innovation in federated learning algorithms, privacy-preserving techniques, and fairness-aware methods will pave the way for its widespread adoption and integration into real-world applications, shaping the future of decentralized machine learning."""

import argparse
import warnings

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

import flwr as fl
import helper as utils
from flwr_datasets import FederatedDataset

if __name__ == "__main__":
    N_CLIENTS = 3

    parser = argparse.ArgumentParser(description="Flower")
    parser.add_argument(
        "--partition-id",
        type=int,
        choices=range(0, N_CLIENTS),
        required=True,
        help="Specifies the artificial data partition",
    )
    args = parser.parse_args()
    partition_id = args.partition_id

    # Load the partition data
    fds = FederatedDataset(dataset="hitorilabs/iris", partitioners={"train": N_CLIENTS})

    dataset = fds.load_partition(partition_id, "train").with_format("pandas")[:]
    X = dataset[["petal_length", "petal_width", "sepal_length", "sepal_width"]]
    y = dataset["species"]
    unique_labels = fds.load_split("train").unique("species")
    # Split the on edge data: 80% train, 20% test
    X_train, X_test = X[: int(0.8 * len(X))], X[int(0.8 * len(X)) :]
    y_train, y_test = y[: int(0.8 * len(y))], y[int(0.8 * len(y)) :]

    # Create LogisticRegression Model
    model = LogisticRegression(
        penalty="l2",
        max_iter=1,  # local epoch
        warm_start=True,  # prevent refreshing weights when fitting
    )

    # Setting initial parameters, akin to model.compile for keras models
    utils.set_initial_params(model, n_features=X_train.shape[1], n_classes=3)

    # Define Flower client
    class IrisClient(fl.client.NumPyClient):
        def get_parameters(self, config):  # type: ignore
            return utils.get_model_parameters(model)

        def fit(self, parameters, config):  # type: ignore
            utils.set_model_params(model, parameters)
            # Ignore convergence failure due to low local epochs
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model.fit(X_train, y_train)
            accuracy = model.score(X_train, y_train)
            return (
                utils.get_model_parameters(model),
                len(X_train),
                {"train_accuracy": accuracy},
            )

        def evaluate(self, parameters, config):  # type: ignore
            utils.set_model_params(model, parameters)
            loss = log_loss(y_test, model.predict_proba(X_test), labels=unique_labels)
            accuracy = model.score(X_test, y_test)
            return loss, len(X_test), {"test_accuracy": accuracy}

    # Start Flower client
    fl.client.start_client(
        server_address="0.0.0.0:8000", client=IrisClient().to_client()
    )