# Dagster Taxi ETL Demo

This project is a small data pipeline demo with Dagster.

The pipeline:
1. Downloads NYC taxi trip data
2. Cleans and aggregates the data
3. Loads results to PostgreSQL
4. Indexes results in Elasticsearch
5. Runs data quality checks

## Tech Stack

- Dagster (orchestration)
- PostgreSQL (metadata DB + warehouse DB)
- pgAdmin (database UI)
- Elasticsearch
- Kibana
- Docker Compose

## Services and Ports

- Dagster UI: `http://localhost:3000`
- pgAdmin: `http://localhost:5050`
- Elasticsearch: `http://localhost:9200`
- Kibana: `http://localhost:5601`
- Warehouse Postgres (from host): `localhost:5433`

There are 8 containers in total:
1. `dagster_postgres`
2. `app_postgres`
3. `pgadmin`
4. `elasticsearch`
5. `kibana`
6. `user_code`
7. `webserver`
8. `daemon`

## Project Structure

- `src/demo_pipeline/assets/` : asset definitions (extract, transform, load)
- `src/demo_pipeline/checks.py` : asset checks
- `src/demo_pipeline/definitions.py` : Dagster `Definitions`, job, schedule, resources
- `src/demo_pipeline/resources.py` : PostgreSQL and Elasticsearch resources
- `docker-compose.yml` : all services
- `dagster.yaml` : Dagster instance config
- `workspace.yaml` : code location config

## Prerequisites

1. Docker Desktop installed and running
2. Docker Compose available

## Quick Start

1. Build and start all services:

```bash
docker compose up -d --build
```

2. Confirm services are running:

```bash
docker compose ps
```

3. Open Dagster UI:
`http://localhost:3000`

4. Wait 10-20 seconds after startup so the code location is fully ready.

## Run the Pipeline in Dagster

1. Open `Assets` in Dagster UI.
2. Click `Materialize all`.
3. Open the run page and watch progress.
4. After success, assets become green.

Main asset flow:

`raw_taxi_data -> cleaned_taxi_data -> hourly_stats -> (taxi_in_postgres + taxi_in_elasticsearch)`

## Data Quality Checks

There are 2 checks:
1. `no_nulls` on `cleaned_taxi_data` (blocking)
2. `positive_rides` on `hourly_stats`

If the blocking check fails, downstream assets do not run.

## Schedule

- Schedule name: `daily_taxi_etl`
- Job name: `taxi_etl_job`
- Cron: every day at `06:00`
- Timezone: `Europe/Istanbul`

## Verify Output

### PostgreSQL (pgAdmin)

1. Open: `http://localhost:5050`
2. Login:
- Email: `admin@demo.com`
- Password: `admin`
3. Connect to warehouse DB and check table:
- `hourly_taxi_stats`

### Kibana

1. Open: `http://localhost:5601`
2. Go to `Discover`
3. Select index/data view: `taxi-hourly-stats`

## Stop and Clean

Stop services:

```bash
docker compose down
```

Stop and remove volumes for a clean restart:

```bash
docker compose down --remove-orphans -v
```
