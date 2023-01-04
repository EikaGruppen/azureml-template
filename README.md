# Template for Azure ML with Python SDK v2

This repository contains an Azure ML template project built using the Python SDK v2. The project covers the following use-cases:

* Setting up a training pipeline with hyperparameter search in order to train a ~~machine learning~~ logistic regression model,
* Deploying a model for batch inference, and 
* Deploying a model for online inference.

We also show you how to provision the required infrastructure using Terraform. The purpose of this is to make it so the template project is easy to set up and run even without much experience with Azure. 

Please be aware that this is not an "Azure ML Tutorial". The purpose here is to provide a template project that could serve as a starting point for new Azure ML projects. The template project is fully functional though, so it can also serve as an example of how the various pieces of functionality fit together. Most of this is already covered in Microsofts own documentation, but there's very few (if any) end-to-end projects like this. Microsofts documentation and examples mostly covers individual pieces of functionality, and this makes it hard to get a sense of how things can look when combined.  The README will cover how to set up and run the template project, but if you're interested in a more in-depth exploration of what is going on you should check out the [blog post](https://oyvind.dev/blog/getting-started-with-azure-ml-and-the-python-sdk/) I've written on it.

## Provisioning

Install and set up Terraform for Azure by following the instructions on the Terraform website.

1. [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/azure-get-started/install-cli)
2. [Build Infrastructure - Terraform Azure Example](https://developer.hashicorp.com/terraform/tutorials/azure-get-started/azure-build)

Proceed by navigating into the `provision/` directory. Execute the following commands: 

1. `az login` 
2. `terraform init`
3. `terraform apply`

This will create all the required resources in Azure. It might take a few minutes to complete.

## Azure ML

### Setup

#### Environment variables

Create a file in the root directory called `.env`. It should look like this: 

```
BATCH_ENDPOINT_NAME="xxx"
ONLINE_ENDPOINT_NAME="xxx"
SA_NAME="xxx"
SA_CONN_STRING="xxx"
SA_CONTAINER_NAME="xxx"
```

* `BATCH_ENDPOINT_NAME` and `ONLINE_ENDPOINT_NAME` can be whatever, but it has to be unique across the entirety of Azure. These will be the names of the REST endpoints your model will be accessible through.
* `SA_NAME`. The name of the storage acccount. Can be found by executing `az storage account list -g azureml-template-rg --query "[].{Name:name}"`.
* `SA_CONN_STRING`. The connection string for storage account. Can be found by executing `az storage account show-connection-string -n ${storage_account_name}`.
* `SA_CONTAINER_NAME`. Can be retrieved by executing `az storage container list --account-name ${storage_account_name} --query "[].{Name:name}"`. The name will be `azureml-blobstore` followed by a bunch of letters and numbers.

#### Configuration file

You should also download `config.json` and place it in your root directory. It can be downloaded from the top-right corner at `ml.azure.com` or from the resource page in the Azure portal. 

#### Python environment

Finally, install all the packages required for interacting running this the template project in Azure ML. This includes

  * `azure-ai-ml`
  * `azure-identity`
  * `azure-storage-blob`
  * `mlflow`
  * `azureml-mlflow`

You should also install `python-dotenv` and `seaborn`, but those packages are specific to the template project, and wouldn't be required in general.

You could also just run `pip install -r requirements.txt`. 

#### Creating and uploading data

Navigate to the `setup/` directory. This directory contains two Python scripts that should be run to create the data and upload them to the cloud.

1. `create_data.py`
2. `upload_data.py`

### Training

Navigate into the `pipeline/` directory. Create the environment that should be used when training by running `create_environment.py`. Register the dataset you uploaded earlier by running `register_training_data.py`. Finally, run `pipeline.py` to run the training pipeline. This will take up to 30 minutes. Later runs will be quicker as long as you don't make any changes to the environment.

### Batch deployment

#### Setting up

Navigate to the `deployment/batch/` directory. Run the scripts in the following order, but verify that the previous step has been completed before moving on to the next one: 

1. `create_batch_endpoint.py`
2. `create_batch_deployment.py`

When you're done, make sure to run `delete_endpoint.py`.  Endpoints can not be managed with Terraform, so you have to make sure that you've deleted them if you want `terraform destroy` to work.

#### Invoke the endpoint

Find your deployment on `ml.azure.com` and retrieve the value in the REST endpoint field. Run `az account get-access-token --resource https://ml.azure.com --query accessToken -o tsv` to get the required token. 

To invoke the endpoint run `python invoke_with_rest.py --uri ${rest_endpoint} --token ${token}`. The output will be saved to the folder specified in the request body.

### Online deployment

#### Setting up

Navigate to the `deployment/online/` directory. Run the scripts in the following order, but verify that the previous step has been completed before moving on to the next one: 

1. `create_online_endpoint.py`
2. `create_online_deployment.py`
3. `set_traffic_rules.py`

When you're done, make sure to run `delete_endpoint.py`.  Endpoints can not be managed with Terraform, so you have to make sure that you've deleted them if you want `terraform destroy` to work.

#### Invoke the endpoint

Find your deployment on `ml.azure.com` and retrieve the value in the REST endpoint field. Run `az ml online-endpoint get-credentials -g azureml-template-rg -w azureml-template-ws -n {endpoint_name} -o tsv` to get the required token. 

To invoke the endpoint run `python invoke_with_rest.py --uri ${rest_endpoint} --token ${token}`. The predictions will be returned by the API.

## Additonal resources

I found the following websites very helpful when piecing all this stuff together:

* [Documentation for Azure ML SDK v2](https://learn.microsoft.com/nb-no/python/api/overview/azure/ai-ml-readme?view=azure-python)
* [Azure ML SDK v2 Examples](https://github.com/Azure/azureml-examples/tree/main/sdk/python)
* [Azure Machine Learning Documentation](https://learn.microsoft.com/en-us/azure/machine-learning/)
* [Command Component YAML Schema](https://learn.microsoft.com/en-us/azure/machine-learning/reference-yaml-component-command)
* [Invoking online endpoints with REST](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-with-rest#invoke-the-endpoint-to-score-data-with-your-model)
* [Invoking batch endpoints with REST](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-batch-with-rest#configure-the-output-location-and-overwrite-settings)




