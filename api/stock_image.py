import io
import pandas as pd
import numpy as np
import mplfinance as mpf
from . import (
    MariaDB,
    select_data_query,
    logger, 
    image_font
)

class StockImage:
    def __init__(self, stock_id: str, limit: int, conditions: str = None):
        self.stock_id = stock_id
        self.limit = limit
        self.conditions = conditions

        condition = f"stock_id = '{self.stock_id}'"
        if self.conditions:
            condition += f"AND {self.conditions}"
        condition += f" ORDER BY Date DESC LIMIT {self.limit}"
        logger.debug(f"conditions: {condition}")
        query = select_data_query("stock_price", condition)
        self.df = MariaDB().export_data(query)
        self.df.set_index(pd.DatetimeIndex(self.df['Date']), inplace=True)
        self.df.sort_index(inplace=True)
    
    def setting_background(self):
        mycolor = mpf.make_marketcolors(
                up = 'r',
                down = 'g',
                edge = 'inherit',
                wick = 'inherit',
                volume = 'inherit'
            )
        mystyle = mpf.make_mpf_style(
                marketcolors = mycolor,
                gridaxis = 'both',
                gridstyle = '--',
                y_on_right = False,
                figcolor = "(0.82, 0.83, 0.85)",
                gridcolor = "(0.82, 0.83, 0.85)"
            )
        return mystyle
    
    def setting_MA(self, days: int, axs, color: str):
        ma = self.df['Close'].rolling(window=days).mean()
        ap = mpf.make_addplot(ma, ax = axs, color = color, width = 1.0)
        return ap
    
    def setting_MACD(self, axs):
        short_ewm = self.df['Close'].ewm(span=12).mean()
        long_ewm = self.df['Close'].ewm(span=26).mean()
        macd = short_ewm - long_ewm
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal
        ap_macd = mpf.make_addplot(macd, ax = axs, color = 'red', width = 1.0, panel = 2)
        ap_signal = mpf.make_addplot(signal, ax = axs, color = 'blue', width = 1.0, panel = 2)
        ap_macd_bar = mpf.make_addplot(
            histogram, 
            type= 'bar', 
            ax= axs, 
            color=['red' if val >= 0 else 'green' for val in histogram], 
            width= 1.0, 
            panel= 2
        )

        return ap_macd, ap_signal, ap_macd_bar
    
    def draw_picture(self):
        # setiing data
        df = self.df
        last_data = df.iloc[-1]
        highest_price = df['High'].max()
        lowest_price = df['Low'].min()

        my_style = self.setting_background()

        logger.info("Buffer open!!")
        img = io.BytesIO()

        fig = mpf.figure(
            style = my_style,
            figsize = (16, 9),
            facecolor = "gray"
        )

        ax1 = fig.add_axes([0.06,0.25,0.88,0.6])
        ax2 = fig.add_axes([0.06,0.15,0.88,0.1], sharex=ax1)
        ax3 = fig.add_axes([0.06,0.05,0.88,0.1], sharex=ax1)

        ax1.set_ylabel('Price')
        ax2.set_ylabel('Volume')
        ax3.set_ylabel('MACD')
#region <text setting>
        fig.text(0.50, 0.94, self.stock_id, **image_font.title_font)
        fig.text(0.12, 0.90, f"{last_data['Date']}", **image_font.normal_label_font)
        fig.text(0.12, 0.86, 'Open/Close', **image_font.normal_label_font)
        fig.text(0.14, 0.86, 
                f'{np.round(last_data["Open"], 3)}/{np.round(last_data["Close"], 3)}', **image_font.large_red_font
        )
        fig.text(0.40, 0.90, 'High:', **image_font.normal_label_font)
        fig.text(0.40, 0.90, f"{last_data['High']}", **image_font.small_red_font)
        fig.text(0.40, 0.86, "Low:", **image_font.normal_label_font)
        fig.text(0.40, 0.86, f"{last_data['Low']}", **image_font.small_green_font)
        fig.text(0.55, 0.90, f"Volume:", **image_font.normal_label_font)
        fig.text(0.55, 0.90, f'{np.round(last_data["Volume"] / 10000, 3)}', **image_font.normal_font)
        fig.text(0.55, 0.86, "Close:", **image_font.normal_label_font)
        fig.text(0.55, 0.86, f"{df.iloc[-2]['Close']}", **image_font.normal_font)
        fig.text(0.70, 0.90, "Highest: ", **image_font.normal_label_font)
        fig.text(0.70, 0.90, f"{highest_price}", **image_font.small_red_font)
        fig.text(0.70, 0.86, "Lowest: ", **image_font.normal_label_font)
        fig.text(0.70, 0.86, f"{lowest_price}", **image_font.small_green_font)
#endregoin

        # call the every plot(MA,MACD)
        ap1 = self.setting_MA(5, ax1, 'red')
        ap2 = self.setting_MA(20, ax1, 'blue')
        ap3 = self.setting_MA(60, ax1, 'yellow')
        ap_macd, ap_signal, ap_macd_bar = self.setting_MACD(ax3)

        mpf.plot(
            df,
            type='candle',
            style= self.setting_background(),
            volume=ax2,
            addplot=[ap1, ap2, ap3, ap_macd, ap_signal, ap_macd_bar],
            ax=ax1,
            # savefig=img
        )
        fig.savefig(img, format='png')
        img.seek(0)
        return img
