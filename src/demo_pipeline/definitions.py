import os
from dagster import Definitions, load_assets_from_modules, EnvVar, ScheduleDefinition, define_asset_job
from .assets import extract, transform, load
from . import checks
from .resources import PostgresResource, ElasticsearchResource

# Load all assets from the 3 modules
all_assets = load_assets_from_modules([extract, transform, load])

# Define the Job and Schedule as mentioned in Slide 8
taxi_job = define_asset_job("taxi_etl_job", selection="*")

taxi_schedule = ScheduleDefinition(
    name="daily_taxi_etl",
    job=taxi_job,
    cron_schedule="0 6 * * *",
    execution_timezone="Europe/Istanbul",
)

defs = Definitions(
    assets=all_assets,
    asset_checks=[checks.no_nulls, checks.positive_rides],
    schedules=[taxi_schedule],
    jobs=[taxi_job],
    resources={
        "pg": PostgresResource(
            host=EnvVar("APP_PG_HOST"),
            user=EnvVar("APP_PG_USER"),
            password=EnvVar("APP_PG_PASSWORD"),
            database=EnvVar("APP_PG_DB"),
        ),
        "es": ElasticsearchResource(host=EnvVar("ES_HOST")),
    },
)