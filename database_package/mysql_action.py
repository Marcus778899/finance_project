import pymysql
import pymysql.cursors
from secret import mysql_database,mysql_host,mysql_password,mysql_user
import pandas as pd


conn = pymysql.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
)
cursor = conn.cursor()

def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Returning \n{func(*args, **kwargs)}")
        print('-' * 50)
        return func(*args, **kwargs)
    return wrapper

def create_table(table_name: str) -> str:
    '''
    return query script
    '''
    table_schema = pd.read_excel(f'./database_package/table_schema.xlsx', sheet_name=table_name)
    table_schema = table_schema.to_dict('records')
    sql = f'CREATE TABLE IF NOT EXISTS {table_name} ('
    for schema in table_schema:
        sql += f'`{schema["column"]}` {schema["data_type"]},'
    sql = sql[:-1] + ');'
    
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

def select_data(table_name: str, columns: list = None) -> str:
    '''
    return query script
    :param table_name: [stock_price, finance_statement]
    '''
    if columns is None:
        query = f'SELECT * FROM {table_name}'
    else:
        query = f'SELECT {", ".join(columns)} FROM {table_name}'

    return query

def stock_id_already_exist(table_name: str) -> list:
    '''
    check stock_id already exist
    '''
    query = f'SELECT DISTINCT(股票代號) FROM {table_name};'
    return query

def execute_query(query: str) -> None:
    '''
    execute query
    '''
    if query is not None:
        try:
            cursor.execute(query)
            conn.commit()
        except Exception as e:
            print(e)

def close_driver():
    cursor.close()
    conn.close()
    