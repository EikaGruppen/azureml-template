from azure.ai.ml import MLClient
from azure.ai.ml.entities import BatchEndpoint
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from pathlib import Path
import os

load_dotenv(Path("..", "..", ".env"))

ml_client = MLClient.from_config(
    credential=AzureCliCredential(), file_name=str(Path("..", "..", "config.json"))
)

model = ml_client.models.get(name="template_model", label="latest")

endpoint = BatchEndpoint(
    name=os.getenv("BATCH_ENDPOINT_NAME"),
    description="Batch endpoint for the template project",
)

ml_client.batch_endpoints.begin_create_or_update(endpoint)
