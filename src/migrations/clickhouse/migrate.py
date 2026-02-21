from clickhouse_migrations.clickhouse_cluster import ClickhouseCluster
from settings import settings


cluster = ClickhouseCluster(
    db_host=settings.clickhouse.host,
    db_port="9000",
    db_user=settings.clickhouse.user,
    db_password=settings.clickhouse.password.get_secret_value(),
    # db_name=settings.clickhouse.name
)

cluster.migrate(
    db_name=settings.clickhouse.name,
    migration_path="migrations/clickhouse",
    create_db_if_no_exists=True,
    multi_statement=True,
)