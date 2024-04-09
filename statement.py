'''
for practice
'''

from __future__ import print_function
from time import sleep
from tqdm import tqdm
from argparse import ArgumentParser
from database_package import mysql_action
from scraping_package import get_stock_list,finance_statement



def progresses():
    list_ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # total要丟int
    progress = tqdm(total=len(list_), desc='Progress')
    for i in list_:
        progress.update(1)
        sleep(1)
        progress.set_description('Progress: {}'.format(i))

def argument():
    parse = ArgumentParser(
        prog='test',
        usage='usage',
        description='a simple demo of argparse',
        epilog='see the docs:https://docs.python.org/3/library/argparse.html'
        )

    parse.add_argument('posl', help='positional argument')
    parse.add_argument('-o', '--optional', 
                    help='optional argument',
                    dest='opt',
                    default='default'
                    )
    parse.add_argument('n', help= 'repaet time', type= int)
    parse.add_argument('-u', '--user-name', dest= 'username', default= 'Marcus')

    args = parse.parse_args()
    print('positional arg: ', args.posl)
    print('optional arg: ', args.opt)

    for i in range(args.n):
        print('Hello, {}'.format(args.username))

def finance_statement_scraping():
    stock_list = get_stock_list()
    stock_list = [stock.split('.')[0] for stock in stock_list]

    sql_action = mysql_action
#region for sql
    create_query = sql_action.create_table('finance_statement')
    sql_action.execute_query(create_query)
    sql_action.conn.commit()
    def input_data(df):
        insert_query = sql_action.insert_data('finance_statement', df).replace("<NA>", "NULL")
        try:
            sql_action.execute_query(insert_query)
            sql_action.conn.commit()
        except Exception as e:
            print(e)
#endregion

    progress = tqdm(total=len(stock_list), desc='Progress')
    for stock_id in stock_list:
        df = finance_statement(stock_id).finance_report()
        progress.update(1)
        if df is not None:
            input_data(df)
        print(f'{stock_id} DONE')
        print('=' * 50)

    sql_action.close_driver()

def testing():
    sql_action = mysql_action
    df = finance_statement('1259').finance_report()
    print(df)
    sql_action.execute_query(sql_action.insert_data('finance_statement', df).replace("<NA>", "NULL"))
    sql_action.conn.commit()

if __name__ == '__main__':
    finance_statement_scraping()