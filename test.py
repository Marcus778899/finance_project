'''
for practice
'''

from __future__ import print_function
from time import sleep
from tqdm import tqdm
from argparse import ArgumentParser
from database_package import mysql_action
from scraping_package import get_stock_list, company_finance_statement



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

def finance_statement(stock_id: str):
    result = company_finance_statement(stock_id)
    if result is not None:
        try:
            query = mysql_action.insert_data('finance_statement', result)
            mysql_action.execute_query(query)
            print('Finance Statement: {} Done'.format(stock_id))
        except Exception as e:
            print(e)
            print('Finance Statement: {} Failed'.format(stock_id))
        print('=' * 50)

if __name__ == '__main__':
    action = mysql_action
    create_query = action.create_table('finance_statement')
    try:
        action.execute_query(create_query)

        stock_list = get_stock_list()
        progress = tqdm(total=len(stock_list), desc='Progress')
        for stock_id in stock_list:
            finance_statement(stock_id)
            progress.update(1)
            sleep(1)
            progress.set_description('Progress: {}'.format(stock_id))
    finally:
        action.close_driver()