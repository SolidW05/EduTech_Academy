from langchain_classic.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from sql_rewriter_chain import sql_rewriter_chain
from ai_models.llm import LLMFactory
from config.database import engine

llm = LLMFactory.gemini()


prompt = PromptTemplate.from_template("""
You are an expert SQL assistant specialized in SQLite.

Your task is to generate ONLY a valid SQLite SQL query to answer the user's question.

IMPORTANT RULES:

1. Return ONLY the SQL query.
2. Do not include explanations.
3. Do not include "Question:" or "SQLQuery:".
4. Use ONLY tables and columns provided in the database schema.
5. NEVER invent tables, columns, relationships, or values.
6. The database engine is SQLite. Do not use PostgreSQL-specific syntax such as:
   - ILIKE
   - SERIAL
   - FULL OUTER JOIN

SEARCH RULES:

7. When searching text fields (names, descriptions, categories, titles, etc.), ALWAYS use LIKE with wildcards.

   Correct:
   WHERE name LIKE '%Python%'

   Incorrect:
   WHERE name = 'Python'
   WHERE name LIKE 'Python'

8. Text searches must consider partial matches because users usually provide keywords, not exact database values.

9. If the user asks about something like:
   "courses about Python"
   "Python courses"
   "courses related to data engineering"

   Search using LIKE on the relevant text columns.

10. When multiple columns could contain the requested information, search across them using OR.

Example:

User:
"Do you have Python courses?"

Correct SQL pattern:

SELECT *
FROM courses
WHERE name LIKE '%Python%'
OR description LIKE '%Python%';


DATABASE SCHEMA:

{table_info}


Question:
{input}

top_k:
{top_k}

Generate SQL:
""")

db = SQLDatabase(engine=engine
                 , include_tables=[
                     'categories',
                     'certificates',
                     'course_instructors',
                     'courses',
                     'enrollments',
                     'instructors',
                     'students'
                 ])

chain_sql = create_sql_query_chain(
    llm=llm,
   db=db,
    prompt=prompt
)

sql_generator = (
    RunnablePassthrough()
    
    .assign(question =  sql_rewriter_chain)
    
    .assign(response = chain_sql)
    
    .pick('response')
)