from pathlib import Path
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Environment
from azure.identity import AzureCliCredential


ml_client = MLClient.from_config(
    credential=AzureCliCredential(), file_name="config.json"
)

environment = Environment(
    name="template_environment",
    image="mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04",
    conda_file=str(Path("conda.yml").resolve()),
    description="Environment belonging to Azure ML Python SDK v2 Template Project",
)

ml_client.environments.create_or_update(environment)
