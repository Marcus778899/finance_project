from scraping_package import stock_scraping
from database_package import mysql_action


sql = mysql_action
table_name = 'stock_price'
drop_query = sql.drop_table(table_name)
create_query = sql.create_table(table_name)
sql.execute_query(drop_query)
sql.execute_query(create_query)

scraping = stock_scraping
results = scraping.main()
for result in results:
    query = None
    query = sql.insert_data(table_name, result)
    sql.execute_query(query)
    