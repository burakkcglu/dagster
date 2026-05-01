import pandas as pd
from dagster import asset

@asset(group_name="transform", compute_kind="pandas")
def cleaned_taxi_data(raw_taxi_data: pd.DataFrame) -> pd.DataFrame:
    """Clean data: remove nulls and negative fares."""
    df = raw_taxi_data.copy()
    df = df.dropna(subset=['tpep_pickup_datetime', 'fare_amount'])
    df = df[df['fare_amount'] > 0]
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.floor('H')
    
    # Calculate tip percentage as mentioned in the presentation
    if 'tip_amount' in df.columns:
        df['tip_pct'] = (df['tip_amount'] / df['fare_amount']).fillna(0)
    
    return df

@asset(group_name="transform", compute_kind="pandas")
def hourly_stats(cleaned_taxi_data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate into hourly statistics."""
    stats = cleaned_taxi_data.groupby('pickup_hour').agg(
        rides=('VendorID', 'count'),
        avg_fare=('fare_amount', 'mean'),
        avg_tip_pct=('tip_pct', 'mean')
    ).reset_index()
    stats['pickup_hour'] = stats['pickup_hour'].astype(str)
    return stats