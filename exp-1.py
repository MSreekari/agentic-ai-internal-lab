import sqlite3
from groq import Groq


# GROQ API KEY

API_KEY = "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"

client = Groq(api_key=API_KEY)


# DATABASE

DATABASE = "company.db"


# CREATE SAMPLE DATABASE

def setup_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary INTEGER
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]

    if count == 0:

        employees = [
            (1, "Rahul", "Engineering", 70000),
            (2, "Priya", "HR", 55000),
            (3, "Arjun", "Engineering", 80000),
            (4, "Sneha", "Finance", 65000),
            (5, "Vikram", "Engineering", 75000)
        ]

        cursor.executemany("""
            INSERT INTO employees
            (id, name, department, salary)
            VALUES (?, ?, ?, ?)
        """, employees)

    connection.commit()
    connection.close()


# LLM FUNCTION

def ask_llm(prompt):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# GET DATABASE SCHEMA

def get_schema():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    tables = cursor.fetchall()

    schema = ""

    for table in tables:

        table_name = table[0]

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = cursor.fetchall()

        schema += f"\nTable: {table_name}\n"

        for column in columns:

            column_name = column[1]
            column_type = column[2]

            schema += f"- {column_name} ({column_type})\n"

    connection.close()

    return schema


# TEXT TO SQL

def generate_sql(question, schema):

    prompt = f"""
You are a Text-to-SQL Agent.

Convert the user's natural language question
into a valid SQLite SQL query.

Database Schema:
{schema}

User Question:
{question}

Rules:

1. Generate only a SQL SELECT query.
2. Do not use INSERT, UPDATE, DELETE, DROP,
   ALTER, CREATE, or other modification commands.
3. Use only tables and columns that exist in the schema.
4. Return ONLY the SQL query.
5. Do not use markdown code fences.
"""

    sql = ask_llm(prompt)

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql


# ============================================================
# VALIDATE SQL
# ============================================================

def validate_sql(sql):

    sql_upper = sql.upper().strip()

    if not sql_upper.startswith("SELECT"):
        return False

    forbidden_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "REPLACE"
    ]

    for keyword in forbidden_keywords:

        if keyword in sql_upper:
            return False

    return True


# EXECUTE SQL

def execute_sql(sql):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:

        cursor.execute(sql)

        rows = cursor.fetchall()

        column_names = [
            description[0]
            for description in cursor.description
        ]

        connection.close()

        return column_names, rows

    except Exception as error:

        connection.close()

        return None, str(error)


# GENERATE FINAL ANSWER

def generate_answer(question, columns, rows):

    data = ""

    for row in rows:
        data += str(row) + "\n"

    prompt = f"""
You are an Answer Generation Agent.

Answer the user's question using the SQL query results.

User Question:
{question}

Columns:
{columns}

Query Results:
{data}

Give a clear and concise natural-language answer.

Do not invent information that is not present
in the query results.
"""

    return ask_llm(prompt)


# MAIN TEXT-TO-SQL WORKFLOW

def run_text_to_sql():

    print("\n==============================================")
    print("          TEXT-TO-SQL WORKFLOW")
    print("==============================================")

    # STEP 0: SETUP DATABASE

    print("\n[0] Setting up database...")

    setup_database()

    print("Database ready.")


    # STEP 1: GET SCHEMA

    print("\n[1] Retrieving database schema...")

    schema = get_schema()

    print("\nDatabase Schema:")
    print(schema)


    # STEP 2: USER QUESTION

    question = input(
        "\nEnter your question about the database: "
    )


    # STEP 3: GENERATE SQL

    print("\n[2] Generating SQL query...")

    sql = generate_sql(
        question,
        schema
    )

    print("\nGenerated SQL:")
    print(sql)

    # STEP 4: VALIDATE SQL

    print("\n[3] Validating SQL query...")

    if not validate_sql(sql):

        print("\nInvalid SQL query.")
        print("Only SELECT queries are allowed.")

        return

    print("SQL query is valid.")


    # STEP 5: EXECUTE SQL

    print("\n[4] Executing SQL query...")

    columns, results = execute_sql(sql)

    if columns is None:

        print("\nSQL execution error:")
        print(results)

        return

    print("\nQuery Results:")

    print(columns)

    for row in results:
        print(row)


   # STEP 6: GENERATE ANSWER

    print("\n[5] Generating final answer...")

    answer = generate_answer(
        question,
        columns,
        results
    )

    print("\nFinal Answer:")
    print(answer)


# PROGRAM START

if __name__ == "__main__":

    run_text_to_sql()