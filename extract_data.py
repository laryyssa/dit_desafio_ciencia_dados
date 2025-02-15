import os
from dotenv import load_dotenv

import httpx
from prefect import flow
import pandas as pd

load_dotenv()

API_URL = os.getenv("API_URL")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")

def get_json_data():
    url = API_URL
    response = httpx.get(url)
    response.raise_for_status()
    repo = response.json()

    return repo["veiculos"]

def json_to_csv(data_json):
    df = pd.DataFrame(data_json)
    df.to_csv("data/data_extract.csv")


@flow(log_prints=True)
def exctract_data():
    data_json = get_json_data()

    json_to_csv(data_json)


if __name__ == "__main__":
    exctract_data.serve(
        name = DEPLOYMENT_NAME,
        interval=60
    )