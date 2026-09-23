from sqlalchemy import create_engine, MetaData
from langchain_community.utilities import SQLDatabase
from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

def get_sql_db() -> SQLDatabase:
    # Restrict inclusion to structured relational tables to prevent SQL agent from querying vector raw stores directly
    return SQLDatabase(
        engine=engine,
        include_tables=["products", "orders", "customers"]
    )