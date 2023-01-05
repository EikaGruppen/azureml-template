from azure.ai.ml import MLClient, Input, load_component
from azure.identity import AzureCliCredential
from azure.ai.ml.dsl import pipeline
from pathlib import Path
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.sweep import LogUniform
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import ModelType

import mlflow

import os

ml_client = MLClient.from_config(
    credential=AzureCliCredential(), file_name=str(Path("..", "config.json"))
)


cluster = "azureml-template-cluster"

train_test_split = load_component(
    source=str(Path("..", "components", "train_test_split.yml"))
)
model_selection = load_component(
    source=str(Path("..", "components", "model_selection.yml"))
)
evaluate_model = load_component(
    source=str(Path("..", "components", "evaluate_model.yml"))
)


@pipeline(default_compute=cluster)
def template_pipeline(
    dataset_input_path,
    train_size,
    num_folds,
):

    split_step = train_test_split(
        dataset_input_path=dataset_input_path,
        train_size=train_size,
        num_folds=num_folds,
    )

    model_selection_step = model_selection(
        train_input_path=split_step.outputs.train_output_path,
        C=LogUniform(min_value=-5, max_value=-1),
    )

    # The result of the various runs is logged on the MLFlow server,
    # but only output from the best run is returned by the step.
    hyperparameter_search = model_selection_step.sweep(
        primary_metric="accuracy",
        goal="maximize",
        sampling_algorithm="random",
        compute=cluster,
    )

    hyperparameter_search.set_limits(
        max_total_trials=2, max_concurrent_trials=2, timeout=60
    )

    evaluate_step = evaluate_model(
        train_input_path=split_step.outputs.train_output_path,
        test_input_path=split_step.outputs.test_output_path,
        # The `outputs` attribute hyperparameter search contains the
        # output of the run that performed best
        model_input_path=hyperparameter_search.outputs.model_output_path,
        params_input_path=hyperparameter_search.outputs.params_output_path,
    )


pipeline_job = template_pipeline(
    dataset_input_path=Input(
        type=AssetTypes.URI_FILE,
        path="azureml://datastores/workspaceblobstore/paths/template_data/training/iris.parquet",
    ),
    train_size=0.8,
    num_folds=3,
)

pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job, experiment_name="template_experiment"
)
