from langchain_core.runnables import RunnableLambda

def validate_sql(sql: str):

    sql = sql.strip()

    if not sql.upper().startswith("SELECT"):
        sql = "SELECT 'Eso no esta disponible'"

    return sql

sql_validator = RunnableLambda(validate_sql)