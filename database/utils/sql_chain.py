from langchain_core.runnables import RunnablePassthrough

from database.utils.sql_executor import sql_executor
from database.utils.sql_generator import sql_generator
from database.utils.sql_validator import sql_validator
from database.utils.sql_response_generator import sql_response_generator

sql_chain = (
    RunnablePassthrough()
    
    .assign(sql_query=lambda x: sql_generator.invoke({
        "question": x["question"],
        "history": x["history"],
    }))

    .assign(
        validated_sql=lambda x: sql_validator.invoke(
            x["sql_query"]
        )
    )

    .assign(
        sql_result=lambda x: sql_executor.invoke(
            x["validated_sql"]
        )
    )

    | sql_response_generator
)

def consultar_base_de_datos(pregunta: str, history:str) -> str:
    return sql_chain.invoke({"question": pregunta,
                             'history': history})


if __name__=="__main__":
    result = sql_chain.invoke({'question':'cuanto cuestan los cursos de python?'})
    
    print(result)