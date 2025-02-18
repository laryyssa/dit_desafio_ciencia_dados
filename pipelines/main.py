import os
from dotenv import load_dotenv

import httpx
from prefect import flow, task
import pandas as pd
from sqlalchemy import create_engine

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

API_URL = os.getenv("API_URL")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
DOCKER_POOL = os.getenv("DOCKER_POOL")

DATABASE_URL = os.getenv("DATABASE_URL")
TABLE_NAME = os.getenv("TABLE_NAME")

DATA_PATH = "./data/data_extract.csv"

@task
def get_json_data(url):
    try:
        response = httpx.get(url)
        response.raise_for_status()
        repo = response.json()

        return repo["veiculos"]
    
    except Exception as e:
        print(f"ERROR - get_json_data: {e}")

@task
def load_json_to_csv(data, csv_path):
    try:
        df = pd.DataFrame(data)
        df.to_csv(csv_path)
    
    except Exception as e:
        print(f"ERROR - load_json_to_csv: {e}")

@task
def load_csv_to_database(database, table, path):
    try:
        engine = create_engine(database)

        df = pd.read_csv(path)
        df.to_sql(table, engine, if_exists='append', index=True)
    
    except Exception as e:
        print(f"ERROR - load_csv_to_database: {e}")


@flow(log_prints=True)
def exctract_data():
    data_json = get_json_data(
        url = API_URL
    )

    load_json_to_csv(
        data = data_json,
        csv_path = DATA_PATH
    )

    load_csv_to_database(
        database = DATABASE_URL,
        table = TABLE_NAME,
        path= DATA_PATH
    )


if __name__ == "__main__":
    exctract_data.serve(
        name = DEPLOYMENT_NAME,
        interval=60
    ) 