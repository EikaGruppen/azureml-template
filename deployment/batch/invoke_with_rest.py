import argparse
from dotenv import load_dotenv
import requests
from pathlib import Path
import os

parser = argparse.ArgumentParser()
parser.add_argument("--uri", type=str, help="The URI of the batch endpoint")
parser.add_argument("--token", type=str, help="The authentication token")

args = parser.parse_args()

scoring_data_path = f"azureml://datastores/workspaceblobstore/paths//template_data/scoring/"
output_data_path = f"azureml://datastores/workspaceblobstore/paths/template_data/deployment/output/"

payload = {
    "properties" : {
        "InputData": {
            "templateInput" : {
                "JobInputType" : "UriFolder",
                "Uri" : scoring_data_path
            }
        },
        "OutputData": {
            "templateOutput" : {
                "JobOutputType" : "UriFile",
                "Uri" : output_data_path
            }
        }
    }
}

print(payload)

headers = {
    "Authorization": f"Bearer {args.token}",
    "Content-Type": "application/json",
    "azureml-model-deployment" : "template-batch-deployment"
}

response = requests.post(
    url = args.uri,
    json = payload,
    headers = headers
)

print(response.content)