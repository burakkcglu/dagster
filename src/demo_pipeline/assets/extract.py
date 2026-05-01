import pandas as pd
import requests
import io
from dagster import asset

@asset(group_name="extract", compute_kind="python")
def raw_taxi_data() -> pd.DataFrame:
    """Download NYC Yellow Taxi data."""
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
    response = requests.get(url, timeout=120)
    df = pd.read_parquet(io.BytesIO(response.content))
    return df.head(10000)