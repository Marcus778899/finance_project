import time
import re

from sqlalchemy import create_engine
import pandas as pd

from ..setting import DB_INFO, send_info, error_handle

class MariaDB:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MariaDB, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance
    
    def _initialize(self, *args, **kwargs):
        self.engine = create_engine(
            f"mysql+pymysql://{DB_INFO['user']}:{DB_INFO['password']}@{DB_INFO['host']}:{DB_INFO['port']}/{DB_INFO['database']}"
        )
        self.conn = self.engine.connect()
        self.cursor = self.conn.connection.cursor()
        send_info("Connect Successful")
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()
        send_info("Connect Close")

    @error_handle
    def execute_query(self, query: str):
        '''
        execute query and commit to database
        no any return
        '''
        self.cursor.execute(query)
        self.conn.commit()
        send_info("Query executed successfully.")

    @error_handle
    def export_data(self, query:str) -> pd.DataFrame:
        '''
        return Dataframe from database
        '''
        start_time = time.time()
        try:
            self.cursor.execute(query)
            df = pd.DataFrame(
                self.cursor.fetchall(),
                columns = [desc[0] for desc in self.cursor.description]
            )
            return df
        
        finally:
            end_time = time.time()
            send_info(f"Query execution time: {end_time - start_time} seconds.")

    @error_handle
    def insert_data(self, table_name: str, df: pd.DataFrame):

        df.to_sql(table_name, self.engine, if_exists='append', index=False)

    @error_handle
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
    
    @error_handle
    def draw_picture_data(self, table_name: str, condition: str = None):
        query = f"SELECT stock_id, Close, Open, High, Low, Volume, Date FROM {table_name}"
        if condition:
            query += f" WHERE {condition};"
        data = self.export_data(query)
        data.set_index(pd.DatetimeIndex(data['Date']), inplace=True)
        data.sort_index(inplace=True)
        return data