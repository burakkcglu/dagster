import pandas as pd
from dagster import asset, MaterializeResult
from ..resources import PostgresResource, ElasticsearchResource

@asset(group_name="load", compute_kind="postgres")
def taxi_in_postgres(hourly_stats: pd.DataFrame, pg: PostgresResource):
    """Load results into PostgreSQL warehouse."""
    pg.write_df(hourly_stats, "hourly_taxi_stats")
    return MaterializeResult(metadata={"table": "hourly_taxi_stats", "row_count": len(hourly_stats)})

@asset(group_name="load", compute_kind="elasticsearch")
def taxi_in_elasticsearch(hourly_stats: pd.DataFrame, es: ElasticsearchResource):
    """Index results into Elasticsearch for Kibana dashboards."""
    es.index_df(hourly_stats, "taxi-hourly-stats")
    return MaterializeResult(metadata={"index": "taxi-hourly-stats", "doc_count": len(hourly_stats)})