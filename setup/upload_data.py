import os
from pathlib import Path
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

load_dotenv(Path("..", ".env"))

conn_str = os.environ["SA_CONN_STRING"]
container_name = os.environ["SA_CONTAINER_NAME"]

training_data_path = Path("..", "data", "iris.parquet")
scoring_data_path = Path("..", "data", "iris_unlabeled.parquet")

blob_service_client = BlobServiceClient.from_connection_string(conn_str)
try:
    container_client = blob_service_client.create_container(container_name)
except ResourceExistsError as e:
    container_client = blob_service_client.get_container_client(container_name)

blob_client = container_client.get_blob_client(blob=str(Path("template_data", "training", training_data_path.name)))
with training_data_path.open(mode="rb") as data:
    blob_client.upload_blob(data, overwrite=True)

blob_client = container_client.get_blob_client(blob=str(Path("template_data", "scoring", scoring_data_path.name)))
with scoring_data_path.open(mode="rb") as data:
    blob_client.upload_blob(data, overwrite=True)