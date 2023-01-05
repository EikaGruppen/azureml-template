from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineDeployment,
    Model,
    Environment,
    CodeConfiguration,
)
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path("..", "..", ".env"))

ml_client = MLClient.from_config(
    credential=AzureCliCredential(), file_name=str(Path("..", "..", "config.json"))
)

model = ml_client.models.get(name="template_model", label="latest")

environment = Environment(
    image="mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04",
    conda_file=str(Path("conda.yml").resolve()),
)

online_deployment = ManagedOnlineDeployment(
    name="template-online-deployment",
    endpoint_name=os.getenv("ONLINE_ENDPOINT_NAME"),
    model=model,
    environment=environment,
    code_configuration=CodeConfiguration(
        code="./code/",
        scoring_script="scoring.py",
    ),
    instance_type="Standard_DS2_v2",
    instance_count=1,
)

ml_client.online_deployments.begin_create_or_update(online_deployment)
