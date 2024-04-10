'''
finance status check
'''
import sys
import os
sys.path.append(os.getcwd())
import pandas as pd
from database_package import mysql_action
from sklearn.preprocessing import MinMaxScaler


def load_data(stock_id : str) -> pd.DataFrame:
    '''
    return query string for data query
    '''
    query = f"SELECT * FROM finance_statement WHERE stock_id={stock_id}"
    sql_action = mysql_action
    sql_action.execute_query(query)
    result = sql_action.cursor.fetchall()
    columns = [desc[0] for desc in sql_action.cursor.description]
    df = pd.DataFrame(result, columns = columns)
    df.set_index('item', inplace=True)
    df.drop(['stock_id'], axis=1, inplace=True)
    df = df.T.reset_index().rename(columns={'index':'year'})

    sql_action.close_driver()
    return df

class feature_enginnering:
    '''
    feature enginnering \n
    item => ['ROA','ROE','Net Profit Margin','Asset Turnover','Equity Multiplier'] \n
    formula url:https://topics.cnyes.com/statement/
    '''
    def __init__(self, data : pd.DataFrame) -> None:
        self.df = data

    # region for calculate formula

    def get_ROA(self) -> float:
        ROA_value = self.df['稅後淨利'] / self.df['總資產']
        return ROA_value.values
    
    def get_ROE(self) -> float:
        ROE_value = self.df['稅後淨利'] / (self.df['總資產'] - self.df['總負債']) 
        return ROE_value.values
    
    def get_net_profit_margin(self) -> float:
        net_profit_margin_value = self.df['稅後淨利'] / self.df['營收']
        return net_profit_margin_value.values
    
    def get_asset_turnover(self) -> float:
        asset_turnover_value = self.df['營收'] / self.df['總資產']
        return asset_turnover_value.values
    
    def get_equity_multiplier(self) -> float:
        equity_multiplier_value = self.df['營收'] / (self.df['總資產'] - self.df['總負債'])
        return equity_multiplier_value.values
    
    # endregion

    def feature_collect(self) -> pd.DataFrame:
        output_df = self.df.copy()
        output_df['ROA'] = self.get_ROA()
        output_df['ROE'] = self.get_ROE()
        output_df['Net_Profit_Margin'] = self.get_net_profit_margin()
        output_df['Asset_Turnover'] = self.get_asset_turnover()
        output_df['Equity_Multiplier'] = self.get_equity_multiplier()
        return output_df

    
if __name__ == "__main__":
    data = load_data('2330')
    action = feature_enginnering(data)
    df = action.feature_collect()
    print(df)
    print(df.columns)
