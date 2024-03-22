from scraping_package import stock_scraping
from database_package import mysql_action

action = stock_scraping

action.test()

action_sql = mysql_action
action_sql.test_conn()