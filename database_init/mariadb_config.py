import os
import logging
import configparser
import pandas as pd
import pymysql

config_file = os.path.join(os.path.dirname(__file__),'loginINFO.cfg')

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

        self.conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        logging.info("MariaDB connection established.")

    def close_driver(self):

        self.cursor.close()
        self.conn.close()
        logging.info("MariaDB connection closed.")

    def insert_data(self, table_name: str, df: pd.DataFrame):

        logging.info(f"Inserting data into {table_name}...")
        
        columns = ', '.join(['`' + col + '`' for col in df.columns])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ("
        
        try:
            self.cursor.execute(
                query,
                [tuple(row) for row in df.itertuples(index = False)]
            )
        except Exception as e:
            logging.error(f"Error inserting data: {e}")
    
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