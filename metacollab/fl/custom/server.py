import flwr as fl
import helper as utils
from sklearn.linear_model import LogisticRegression


if __name__ == "__main__":
    model = LogisticRegression()
    utils.set_initial_params(model, n_classes=3, n_features=4)
    strategy = fl.server.strategy.FedAvg(
        min_available_clients=2,
        fit_metrics_aggregation_fn=utils.weighted_average,
        evaluate_metrics_aggregation_fn=utils.weighted_average,
    )
    fl.server.start_server(
        server_address="0.0.0.0:8000",
        strategy=strategy,
        config=fl.server.ServerConfig(num_rounds=25),
    )