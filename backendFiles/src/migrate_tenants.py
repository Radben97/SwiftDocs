import os
import sys
import subprocess
from sqlalchemy import create_engine,text
from alembic.config import Config
from alembic import command
root_dir = os.path.dirname(os.path.abspath(__file__))
db_url = "postgresql+psycopg2://postgres:Pin05almm@localhost:5432/swiftdocsdb"

def get_all_current_schemas():
    if not db_url:
        raise Exception("database url not found")
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text(
            """
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name NOT IN ('public', 'information_schema', 'pg_catalog', 'pg_toast')
            AND schema_name LIKE 'tenant_%'
            """
        ))
        return [row[0] for row in result]
    
def create_tenant_schema(tenant_name):
    if not db_url:
        raise Exception("database url not found")
    engine = create_engine(db_url)
    try:
        with engine.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {tenant_name}"))
        print(f"{tenant_name} schema successfully created")
    except Exception as e:
        print(e)

def migrate_tenant_schema(tenant_name):
    print(f"migrating tenant: {tenant_name}")
    try:
        ini_path = os.path.join(root_dir,"..","migrations-tenant","alembic.ini")
        cfg = Config(ini_path)
        cfg.attributes['tenant_schema'] = tenant_name
        print("running migration script")
        command.upgrade(cfg,"head")
        print("migrated successfully")
    except Exception as e:
        print(e)
    

