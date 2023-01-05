from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    BatchDeployment,
    CodeConfiguration,
    BatchRetrySettings,
    Environment,
)
from dotenv import load_dotenv
from azure.ai.ml.constants import BatchDeploymentOutputAction
from azure.identity import AzureCliCredential
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

deployment = BatchDeployment(
    name="template-batch-deployment",
    description="Batch deployment for the template project",
    endpoint_name=os.getenv("BATCH_ENDPOINT_NAME"),
    model=model,
    environment=environment,
    code_configuration=CodeConfiguration(
        code="./code/",
        scoring_script="scoring.py",
    ),
    compute="azureml-template-cluster",
    instance_count=1,
    max_concurrency_per_instance=1,
    mini_batch_size=1,
    output_action=BatchDeploymentOutputAction.SUMMARY_ONLY,
    retry_settings=BatchRetrySettings(max_retries=3, timeout=300),
    logging_level="info",
)

ml_client.batch_deployments.begin_create_or_update(deployment)
