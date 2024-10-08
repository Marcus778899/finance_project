import os
import json
from . import logger

table_schema_file = os.path.join(
    os.path.dirname(__file__),
    'table_schema.json'
)

def debug(func):
    def wrapper(*args, **kwargs):
        logger.info(f"""
Executing {func.__name__}
Args: {args}
Kwargs: {kwargs}
Return: {func(*args, **kwargs)}
"""
        )
        return func(*args, **kwargs)
    return wrapper

@debug
def create_table_query(table_name: str) -> str:
    with open(table_schema_file, 'r') as f:
        table_schema = json.load(f)[table_name]
    
    columns = []
    condition = ""

    for key, value in table_schema.items():
        if key == "Condition":
            if value != "None":
                condition = value
        else:
            columns.append(f"{key} {value}")
    
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    query += ", ".join(columns)
    
    if condition:
        query += f", {condition}"
    
    query += ");"
    
    return query

@debug
def select_data_query(table_name: str, condition: str = None):
    query = f"SELECT stock_id, Close, Open, High, Low, Volume, Date FROM {table_name}"
    if condition:
        query += f" WHERE {condition};"
    return query

@debug
def delete_data_query(table_name: str, condition: str):
    query = f"DELETE FROM {table_name} WHERE {condition};"
    return query