import os
import logging
import json
import numpy
from pathlib import Path
import mlflow


def init():
    global model
    model_path = Path(os.environ["AZUREML_MODEL_DIR"], "model")
    model = mlflow.sklearn.load_model(model_path)
    logging.info("Init complete")


def run(raw_data):
    logging.info("Request received")
    data = json.loads(raw_data)["data"]
    data = numpy.array(data)
    result = model.predict(data)
    logging.info("Request processed")
    return result.tolist()
