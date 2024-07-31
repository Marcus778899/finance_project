from database_init import MariaDB
from src import get_stock_list

db = MariaDB()

db.create_table("stock_list")
stock_list = get_stock_list.main()
db.insert_data("stock_list", stock_list)

db.close_driver()