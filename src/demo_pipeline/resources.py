import pandas as pd
import sqlalchemy as sa
from dagster import ConfigurableResource
from elasticsearch import Elasticsearch, helpers

class PostgresResource(ConfigurableResource):
    host: str
    user: str
    password: str
    database: str
    port: int = 5432

    def get_engine(self):
        return sa.create_engine(f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")

    def write_df(self, df: pd.DataFrame, table_name: str):
        engine = self.get_engine()
        df.to_sql(table_name, engine, if_exists="replace", index=False)

class ElasticsearchResource(ConfigurableResource):
    host: str

    def get_client(self):
        return Elasticsearch(self.host)

    def index_df(self, df: pd.DataFrame, index_name: str):
        es = self.get_client()
        documents = df.to_dict(orient="records")
        helpers.bulk(es, [{"_index": index_name, "_source": doc} for doc in documents])