from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool,text
from alembic import context
from src.database import schema_base,public_base
import src.models.models
from src.migrate_tenants import get_all_current_schemas
import os

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = public_base.metadata


def multi_tenant_migration():
        print("single_tenant func running")
        schemas = get_all_current_schemas()
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        

        with connectable.connect() as connection:
            for schema in schemas:
                connection.execute(text(f"SET search_path TO {schema} "))
                connection.commit()
                context.configure(
                    connection=connection,
                    target_metadata=target_metadata,
                    include_schemas=True
                )
                with context.begin_transaction():
                    context.run_migrations()

def single_tenant_migration(schema):
            print("single_tenant func running")
            connectable = engine_from_config(
                config.get_section(config.config_ini_section, {}),
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
            )

            with connectable.connect() as connection:
                connection.execute(text(f"SET search_path TO {schema} "))
                connection.commit()
                context.configure(
                    connection=connection,
                    target_metadata=target_metadata
                )

                with context.begin_transaction():
                    context.run_migrations()     

def run_migrations_online() -> None:
    tenant_Schema = context.config.attributes.get("tenant_schema",None)
    if tenant_Schema:
         single_tenant_migration(tenant_Schema)
    else:
         multi_tenant_migration()


run_migrations_online()


