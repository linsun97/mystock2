from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
import time
from sqlalchemy import create_engine
import email.message
from flask import redirect, url_for, request

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
    df_breaks =[x for x in all_d_list if x not in df_i_list]
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
    fig.add_trace(go.Line(x=df.index, y=df['kwr'],name="20天k線波動率",marker_color="red",opacity=0.5,yaxis="y3"))
    fig.add_trace(go.Line(x=df.index, y=df['updown'],name="50天振幅",marker_color="orange",opacity=0.5,yaxis="y4"))
    fig.add_trace(go.Line(x=df.index, y=df['rs'],name="50天相對強度PR值",marker_color="green",opacity=0.5,yaxis="y5"))
    fig.add_trace(go.Line(x=df.index, y=df['rci'],name="20天rci值",marker_color="purple",opacity=0.5,yaxis="y6"))
    fig.add_trace(go.Bar(x=df.index, y=df['nh'].str.len(),name="創新高",marker_color="gray",opacity=0.5,yaxis="y7"))


    fig.update_layout(
        height=1200,
        yaxis={'domain': [0.56, 1]} ,
        yaxis2={'domain': [0.45, 0.55]} ,
        yaxis3={'domain': [0.36, 0.44]} ,
        yaxis4={'domain': [0.27, 0.35]} ,
        yaxis5={'domain': [0.18, 0.26]} ,
        yaxis6={'domain': [0.09, 0.17]} ,
        yaxis7={'domain': [0, 0.08]} ,
        title=f"{stockid}日線圖",
        # xaxis_rangeslider_visible=False
    )


    fig.update_xaxes(rangebreaks=[{"values": df_breaks}],showspikes=True,spikecolor="gray",spikethickness=1,spikesnap="cursor",spikemode="across",spikedash="solid")
    fig.update_yaxes(showspikes=True,spikecolor="gray",spikethickness=1,spikesnap="cursor",spikemode="across",spikedash="solid")
    # fig.show()
    fig.show()

    return fig
    
# stockid = request.args.get('stockid')
# pic_k("6762")