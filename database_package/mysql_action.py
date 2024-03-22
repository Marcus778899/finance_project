import pymysql
import pymysql.cursors
from secret import key
import pandas as pd

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

def test_conn():
    conn,cursor = next(get_conn())
    conn.ping(reconnect=True)
    cursor.execute('SHOW DATABASES')
    conn.commit()

def create_table(table_name: str):
    conn, cursor = next(get_conn())
    conn.ping(reconnect=True)
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name}(stock_id VARCHAR(10) PRIMARY KEY, stock_name VARCHAR(20), stock_type VARCHAR(10))')
    conn.commit()
    print(f'Create table {table_name} Done')