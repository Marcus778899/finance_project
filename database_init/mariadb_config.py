import os
import logging
import json
import configparser
import pandas as pd
from sqlalchemy import create_engine

config_file = os.path.join(os.path.dirname(__file__),'loginINFO.cfg')
table_schema_file = os.path.join(os.path.dirname(__file__), 'table_schema.json')

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

        logging.info("MariaDB connection established.")

    def close_driver(self):

        self.cursor.close()
        self.conn.close()
        self.engine.dispose()
        logging.info("MariaDB connection closed.")

    def create_table(self, table_name: str):
        with open (table_schema_file, 'r') as f:
            table_schema = json.load(f)[table_name]

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for key, value in table_schema.items():
            query += f"{key} {value}, "
        query = query[:-2] + ");"
        
        try:
            self.cursor.execute(query)
            self.conn.commit()
            logging.info(f"Table {table_name} created successfully.")
        except Exception as e:
            logging.warning(f"Error creating table: {e}")

    def insert_data(self, table_name: str, df: pd.DataFrame):

        try:
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

        logging.info("Data insertion completed.")

    def select_data(self, query: str) -> pd.DataFrame:

        logging.info(f"Executing query: {query}")

        try:
            self.cursor.execute(query)
            df = pd.DataFrame(
                self.cursor.fetchall(),
                columns = [desc[0] for desc in self.cursor.description]
            )
            return df
        
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return None
        
    def delete_data(self, table_name: str, condition: str):

        logging.info(f"Deleting data from {table_name} where {condition}...")
        query = f"DELETE FROM {table_name} WHERE {condition}"

        try:
            self.cursor.execute(query)
            self.conn.commit()
            logging.info(f"Data deleted successfully.\nCondition is {condition}")
        except Exception as e:
            logging.error(f"Error deleting data: {e}")