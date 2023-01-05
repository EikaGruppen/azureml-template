from azure.ai.ml import MLClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path("..", "..", ".env"))

ml_client = MLClient.from_config(
    credential=AzureCliCredential(), file_name=str(Path("..", "..", "config.json"))
)

ml_client.online_endpoints.begin_delete(name=os.getenv("ONLINE_ENDPOINT_NAME"))
