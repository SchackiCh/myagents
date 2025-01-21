from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Float,
    insert,
    inspect,
    text,
)

engine = create_engine("sqlite:///:memory:")
metadata_obj = MetaData()

# create city SQL table
table_name = "receipts"
receipts = Table(
    table_name,
    metadata_obj,
    Column("receipt_id", Integer, primary_key=True),
    Column("customer_name", String(16), primary_key=True),
    Column("price", Float),
    Column("tip", Float),
)
metadata_obj.create_all(engine)

rows = [
    {"receipt_id": 1, "customer_name": "Alan Payne", "price": 12.06, "tip": 1.20},
    {"receipt_id": 2, "customer_name": "Barack Obama", "price": 23.86, "tip": 0.24},
    {"receipt_id": 3, "customer_name": "Woodrow Wilson", "price": 53.43, "tip": 5.43},
    {"receipt_id": 4, "customer_name": "Real estate GmbH", "price": 21.11, "tip": 1.00},
]

for row in rows:
    stmt = insert(receipts).values(**row)
    with engine.begin() as connection:
        cursor = connection.execute(stmt)

inspector = inspect(engine)
columns_info = [(col["name"], col["type"]) for col in inspector.get_columns("receipts")]

table_description = "Columns:\n" + "\n".join([f"  - {name}: {col_type}" for name, col_type in columns_info])
print(table_description)

from smolagents import tool

@tool
def sql_engine(query: str) -> str:
    """
    Allows you to perform SQL queries on the table. Returns a string representation of the result.
    The table is named 'receipts'. Its description is as follows:
        Columns:
        - receipt_id: INTEGER
        - customer_name: VARCHAR(16)
        - price: FLOAT
        - tip: FLOAT

    Args:
        query: The query to perform. This should be correct SQL.
    """
    output = ""
    with engine.connect() as con:
        rows = con.execute(text(query))
        for row in rows:
            output += "\n" + str(row)
    return output

table_name = "waiters"
receipts = Table(
    table_name,
    metadata_obj,
    Column("receipt_id", Integer, primary_key=True),
    Column("waiter_name", String(16), primary_key=True),
)
metadata_obj.create_all(engine)

rows = [
    {"receipt_id": 1, "waiter_name": "Corey Johnson"},
    {"receipt_id": 2, "waiter_name": "Michael Watts"},
    {"receipt_id": 3, "waiter_name": "Michael Watts"},
    {"receipt_id": 4, "waiter_name": "Margaret James"},
]
for row in rows:
    stmt = insert(receipts).values(**row)
    with engine.begin() as connection:
        cursor = connection.execute(stmt)

        updated_description = """Allows you to perform SQL queries on the table. Beware that this tool's output is a string representation of the execution output.
It can use the following tables:"""

inspector = inspect(engine)
for table in ["receipts", "waiters"]:
    columns_info = [(col["name"], col["type"]) for col in inspector.get_columns(table)]

    table_description = f"Table '{table}':\n"

    table_description += "Columns:\n" + "\n".join([f"  - {name}: {col_type}" for name, col_type in columns_info])
    updated_description += "\n\n" + table_description

print(updated_description)


from smolagents import CodeAgent, HfApiModel

sql_engine.description = updated_description

agent = CodeAgent(
    tools=[sql_engine],
    model=HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct"),
    #model=HfApiModel("meta-llama/Meta-Llama-3.1-8B-Instruct"),
)

agent.run("Which waiter got more total money from tips?")

#agent.run("Can you give me the client name of the most expensive receipt?")
### WOW agent.run("Can you give me the customer name with the highest percent of tip compared to the price?")

### Oida das liefert die falsche Antwort:  Out - Final answer: 51.7968 ---> Aber die gleiche Frage mit . am Schluss macht es richtig!! 4.7783999999999995
##agent.run("Can you give me the highest tip amount and convert it from $ to €")
##agent.run("Can you give me the highest tip amount and convert it from $ to €.")

##agent.run("Can you give me the highest tip amount and convert it from $ to €. Show the price as € and as $")


##agent.run("Gib mir eine Liste der Kunden, die mehr als 10% Trinkgeld gegeben haben.")


##agent.run("Gib mir eine Liste der Kunden, die Präsident der Vereinigten Staaten waren.")
##agent.run("Gib mir eine Liste der Kunden, die Präsident der Vereinigten Staaten waren. Inklusive News über die Präsidenten.")

##Gutes Beispiel für die 2 llms 
##agent.run("Gib mir eine Liste der Kunden, die Präsident der Vereinigten Staaten waren. Inklusive Geburtsjahr")

##agent.run("Wieviel Geld war es insgesamt und wieviel Trinkgeld wurde insgesamt gegeben?")

