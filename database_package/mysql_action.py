import pymysql
import pymysql.cursors
from secret import key
import pandas as pd
from datetime import datetime

def get_conn():
    conn = pymysql.connect(
        host=key.mysql_host,
        user=key.mysql_user,
        password=key.mysql_password,
        database=key.mysql_database,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )
    cursor = conn.cursor()
    try:
        yield conn, cursor
    finally:
        conn.close()

def create_table(table_name: str) -> str:
    '''
    return query script
    '''
    table_schema = pd.read_excel(f'./database_package/table_schema.xlsx', sheet_name=table_name)
    table_schema = table_schema.to_dict('records')
    sql = f'CREATE TABLE IF NOT EXISTS {table_name} ('
    for schema in table_schema:
        sql += f'`{schema["column"]}` {schema["data_type"]},'
    sql = sql[:-1] + ')'
    
    return sql

def insert_data(table_name: str, data: pd.DataFrame) -> str:
    '''
    return query script
    '''
    if data is None:
        return None
    else:
        columns = ', '.join(['`' + col + '`' for col in data.columns])
        query = f"INSERT INTO {table_name} ({columns}) VALUES "
        for _, row in data.iterrows():
            query += f'{tuple(row)},'
        query = query[:-1] + ';'

        return query

def drop_table(table_name: str) -> str:
    '''
    return query script
    '''
    query = f'DROP TABLE {table_name}'

    return query


def execute_query(query: str) -> None:
    '''
    execute query
    '''
    if query is not None:
        conn, cursor = next(get_conn())
        conn.ping(reconnect=True)
        cursor.execute(query)
        conn.commit()
        print(f'Query executed: \n{query}')
