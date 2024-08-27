import io
import pandas as pd
import mplfinance as mpf
from . import MariaDB,select_data_query,logger

def draw_stock_history(stock_id: str, limit: int, conditions: str = None):
    '''
    condition:
    <column> = <value>
    example:
    Date = '2022-01-01'
    p.s. don't add ";"
    '''
    condition = f"stock_id = '{stock_id}'"
    if conditions:
        condition += f"AND {conditions}"
    condition += f" ORDER BY Date DESC LIMIT {limit}"

    query = select_data_query("stock_price",condition)
    df = MariaDB().export_data(query)
    df.set_index(pd.DatetimeIndex(df['Date']), inplace=True)
    df.sort_index(inplace=True)

    # save image in buffer
    logger.info("Buffer open!!")
    img = io.BytesIO()

    mpf.plot(
        df,
        title=stock_id,
        type='candle',
        style='charles',
        mav=[5,20],
        mavcolors=['blue','yellow'],
        figscale=1.2,
        volume=True,
        savefig=img
        )

    img.seek(0)

    return img

