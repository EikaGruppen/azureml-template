import os
import mlflow
import pandas as pd
from pathlib import Path


def init():
    global model
    global output_path

    # The model is read from this folder
    model_path = Path(os.environ["AZUREML_MODEL_DIR"], "model")
    # The output should be written to this folder
    output_path = os.environ["AZUREML_BI_OUTPUT_PATH"]
    model = mlflow.sklearn.load_model(model_path)


# `mini_batch` is a list of paths within the folder the endpoint was invoked with
def run(mini_batch):
    data = pd.concat([pd.read_parquet(file_path) for file_path in mini_batch])

    X = data.to_numpy()
    pred = model.predict(X)
    data["pred_species"] = pred

    output_file_path = Path(output_path, "iris_predictions.parquet")
    data.to_parquet(output_file_path)

    return mini_batch
