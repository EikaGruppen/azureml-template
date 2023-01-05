from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineEndpoint
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path("..", "..", ".env"))

ml_client = MLClient.from_config(
    credential=AzureCliCredential(), file_name=str(Path("..", "..", "config.json"))
)

endpoint = ManagedOnlineEndpoint(
    name=os.getenv("ONLINE_ENDPOINT_NAME"),
    auth_mode="aml_token",
)

ml_client.online_endpoints.begin_create_or_update(endpoint)
