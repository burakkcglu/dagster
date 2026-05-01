from dagster import asset_check, AssetCheckResult
import pandas as pd

@asset_check(asset="cleaned_taxi_data", blocking=True)
def no_nulls(cleaned_taxi_data: pd.DataFrame):
    """Ensure no null values exist in pickup times. Blocking check."""
    null_count = cleaned_taxi_data['tpep_pickup_datetime'].isna().sum()
    return AssetCheckResult(
        passed=bool(null_count == 0), 
        metadata={"null_records": int(null_count)}
    )

@asset_check(asset="hourly_stats")
def positive_rides(hourly_stats: pd.DataFrame):
    """Ensure all hours have at least 1 ride."""
    bad_rows = (hourly_stats['rides'] <= 0).sum()
    return AssetCheckResult(
        passed=bool(bad_rows == 0), 
        metadata={"bad_rows": int(bad_rows)}
    )