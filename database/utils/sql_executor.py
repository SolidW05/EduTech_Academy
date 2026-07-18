from langchain_core.runnables import RunnableLambda
from sqlalchemy import text
from config.database import engine

def execute_sql(sql: str):

    with engine.connect() as conn:
        result = conn.execute(text(sql))

        return result.mappings().all()

sql_executor = RunnableLambda(execute_sql)