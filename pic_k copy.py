from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
import time
from sqlalchemy import create_engine
import email.message

engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock",pool_size=100,pool_recycle=3600, max_overflow=40,echo=False)
def pic_k(stockid):
    pd.set_option("display.float_format",'{:.2f}'.format)
    df = pd.read_sql(f'st_{stockid}',engine)
    df.index = df['up_date'].dt.strftime('%Y-%m-%d')

    # print(df)
    # quit()
    all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    all_dates = all_dates.strftime('%Y-%m-%d')
    all_d_list = all_dates.tolist()
    # print(x)
    # quit()
    df_i_list = df.index.tolist()
    # print(y)
    # quit()
    # df.index = pd.to_datetime(df.index)
    # all_dates = pd.to_datetime(all_dates)
    # breaks = all_dates[~all_dates.isin(df.index)]
    breaks =[x for x in all_d_list if x not in df_i_list]
    # breaks = all_dates[~all_dates.map(lambda x: x.strftime('%Y-%m-%d')).isin(df.index.tolist())]
    df_breaks = breaks
    # print(df_breaks)
    # quit()
    df['MA20'] = df['over'].rolling(window=20).mean()
    df['MA50'] = df['over'].rolling(window=50).mean()


    fig = go.Figure(data=[go.Candlestick(x=df.index, 
                                        open = df['open'],
                                        high = df['high'],
                                        low = df['low'],
                                        close = df['over'],
                                        increasing_line_color='red', 
                                        decreasing_line_color='green')])


    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MA20'],
        name='20日均线'
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MA50'],
        name='50日均线'
    ))


    fig.add_trace(go.Bar(x=df.index, y=df['volume'],name="成交量",marker_color="blue",opacity=0.5,yaxis="y2"))


    fig.update_layout(
        height=800,
        yaxis={'domain': [0.35, 1]} ,
        yaxis2={'domain': [0.15, 0.3]} ,
        title=f"日線圖",
        # xaxis_rangeslider_visible=False
    )


    fig.update_xaxes(rangebreaks=[{"values": df_breaks}],showspikes=True,spikecolor="gray",spikethickness=1,spikesnap="cursor",spikemode="across",spikedash="solid")
    fig.update_yaxes(showspikes=True,spikecolor="gray",spikethickness=1,spikesnap="cursor",spikemode="across",spikedash="solid")
    # fig.show()

    return fig


