from pathlib import Path
import os

from dotenv import load_dotenv
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
from azure.identity import AzureCliCredential
from azure.ai.ml import MLClient

load_dotenv(Path("..", ".env"))

account_name = os.environ["SA_NAME"]
container_name = os.environ["SA_CONTAINER_NAME"]

ml_client = MLClient.from_config(
    credential = AzureCliCredential(),
    file_name = "config.json"
    )

iris_data = Data(
    path=f"https://{account_name}.blob.core.windows.net/{container_name}/template_data/training/iris.parquet",
    type=AssetTypes.URI_FILE,
    description="Iris dataset for use in Azure ML Template Project",
    name="template_data_iris"
)

ml_client.data.create_or_update(iris_data)
