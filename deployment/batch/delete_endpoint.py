from azure.ai.ml import MLClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path("..", "..", ".env"))

ml_client = MLClient.from_config(
    credential=AzureCliCredential(), file_name=str(Path("..", "..", "config.json"))
)

ml_client.batch_endpoints.begin_delete(name=os.getenv("BATCH_ENDPOINT_NAME"))
