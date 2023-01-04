import argparse
from dotenv import load_dotenv
import requests
from pathlib import Path
import os
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--uri", type=str, help="The URI of the batch endpoint")
parser.add_argument("--token", type=str, help="The authentication token")

args = parser.parse_args()

headers = {
    "Authorization": f"Bearer {args.token}",
    "Content-Type": "application/json"
}

dat = pd.read_parquet(Path("..", "..", "data", "iris_unlabeled.parquet"))

payload = {
    "data" : dat.values.tolist()
}

response = requests.post(
    url = args.uri,
    json = payload,
    headers = headers
)

print(response.content)