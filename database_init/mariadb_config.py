import os
import re
import configparser
from time import time
import pandas as pd
from sqlalchemy import create_engine
from . import logger

config_file = os.path.join(
    os.path.dirname(__file__),
    'loginINFO.cfg'
    )
table_schema_file = os.path.join(
    os.path.dirname(__file__), 
    'table_schema.json'
    )

if config_file:
    config = configparser.ConfigParser()
    config.read(config_file)
    host = config.get('DB_Config', 'HOST')
    port = config.get('DB_Config', 'PORT')
    user = config.get('DB_Config', 'USERNAME')
    password = config.get('DB_Config', 'PASSWORD')
    database = config.get('DB_Config', 'DATABASE')

class MariaDB:
    def __init__(self):
        self.engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
        self.conn = self.engine.connect()
        self.cursor = self.conn.connection.cursor()
        logger.debug("MariaDB connection established.")

    def __del__(self):

        self.cursor.close()
        self.conn.close()
        self.engine.dispose()
        logger.debug("MariaDB connection closed.")

    def execute_query(self, query: str):
        '''
        execute query and commit to database
        no any return
        '''
        try:
            self.cursor.execute(query)
            self.conn.commit()
            logger.debug("Query executed successfully.")
        except Exception as e:
            logger.exception(f"Error executing query: {e}")

    def export_data(self, query:str) -> pd.DataFrame:
        '''
        return Dataframe from database
        '''
        start_time = time()
        try:
            self.cursor.execute(query)
            df = pd.DataFrame(
                self.cursor.fetchall(),
                columns = [desc[0] for desc in self.cursor.description]
            )
            return df
        
        except Exception as e:
            logger.exception(f"Error executing query: {e}")
            return None
        finally:
            end_time = time()
            logger.info(f"Query execution time: {end_time - start_time} seconds.")

    def insert_data(self, table_name: str, df: pd.DataFrame):

        try:
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            logger.info(f"Data inserted into {table_name} successfully.")
        except Exception as e:
            logger.exception(f"Error inserting data: {e}")

        logger.debug("Data insertion completed.")

    def parse_basic_info(self) -> list[str]:
        '''
        return stock item list
        '''
        df = self.export_data("SELECT * FROM basic_info;")
        df = df.set_index('stock').to_dict()['category_market']
        stock_list = []
        for key, value in df.items():
            stock_code = re.findall(r'^[A-Za-z0-9]+', key)[0]
            if value == '上市':
                stock_list.append(f"{stock_code}.TW")
            if value == '上櫃':
                stock_list.append(f"{stock_code}.TWO")
        return stock_list
    
if __name__ == '__main__':
    db = MariaDB()
    print(db.parse_basic_info())