from urllib import request as req
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bs
import pandas as pd
from enum import Enum
from io import StringIO


class type_category(Enum):
    monthly_revenue = 'monthly-revenue'
    eps = 'eps'
    net_value = 'nav'
    income_statement = 'income-statement'
    assets = 'assets'
    liabilities_and_equity = 'liabilities-and-equity'
    cash_flow = 'cash-flow-statement'
    dividend = 'dividend-policy'

def get_url(stock_id: str, type: type_category) -> str:
    return f'https://statementdog.com/analysis/{stock_id}/{type.value}'

def scraping_finance_statement(stock_id: str, type: type_category) -> pd.DataFrame:
    try:
        url = get_url(stock_id, type)
        res = req.urlopen(url)
        soup = bs(res, 'html.parser')
        div = soup.find('div', {'class': 'datasheet-for-seo'})
        table_html = str(div)
        df = pd.read_html(StringIO(table_html))[0]
        return df

    except HTTPError as e:
        if e.code == 404:
            print(f"Can\'t find {stock_id}")
        else:
            print(f'Else Error')


class FinanceScraping:
    def __init__(self, stock_id: str) -> None:
        self.stock_id = stock_id
        
        self.statement_sheet = [
            type_category.income_statement,
            type_category.assets,
            type_category.liabilities_and_equity,
            type_category.cash_flow,
        ]

        self.profit = [
            type_category.monthly_revenue,
            type_category.eps,
            type_category.net_value
        ]

    def finance_report(self) -> pd.DataFrame:
        sheet = pd.DataFrame()
        for type in self.statement_sheet:
            df = scraping_finance_statement(self.stock_id, type)
            if df is None:
                return None
            sheet = pd.concat([sheet, df], ignore_index=True)

        sheet.columns = sheet.columns.str.replace('季度', 'item')
        sheet['stock_id'] = self.stock_id
        sheet.replace("無", pd.NA, inplace=True)
        return sheet

    def dividend_report(self) -> pd.DataFrame:
        dividend = scraping_finance_statement(self.stock_id, type_category.dividend)
        if dividend is None:
            return None
        return dividend

if __name__ == '__main__':
    action = FinanceScraping('0050')
    df = action.finance_report()
    print(df)
    print(df.dtypes)
    