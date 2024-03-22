from scraping_package import stock_scraping
from database_package import mysql_action
import pandas as pd

action = stock_scraping

test = action.test()

action_sql = mysql_action
table_name = 'stock_price'
create_query = action_sql.create_table(table_name)
insert_query = action_sql.insert_data(table_name, test)
action_sql.execute_query(create_query)
action_sql.execute_query(insert_query)