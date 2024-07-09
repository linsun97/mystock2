from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
import time
from sqlalchemy import create_engine
import email.message

engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock",pool_size=100,pool_recycle=3600, max_overflow=40,echo=False)
pd.set_option("display.float_format",'{:.2f}'.format)
def pic_k_w(stockid):
    df = pd.read_sql(f'st_{stockid}',engine)
    df.index = df['up_date'].dt.strftime('%Y-%m-%d')

 # -------------------週線圖------------------
    df1 = df.resample('W', on='up_date').agg({'open':'first','high':'max','low':'min','over':'last','volume':'sum'}).reset_index()
    df1['MA10'] = df1['over'].rolling(window=10).mean()
    df1['MA20'] = df1['over'].rolling(window=20).mean()



    fig2 = go.Figure(data=[go.Candlestick(x=df1['up_date'], 
                                        open = df1['open'],
                                        high = df1['high'],
                                        low = df1['low'],
                                        close = df1['over'],
                                        increasing_line_color='red', 
                                        decreasing_line_color='green')])

    fig2.add_trace(go.Scatter(
        x=df1['up_date'],
        y=df1['MA10'],
        name='10週均线'
    ))

    fig2.add_trace(go.Scatter(
        x=df1['up_date'],
        y=df1['MA20'],
        name='20週均线'
    ))

    fig2.add_trace(go.Bar(x=df1['up_date'], y=df1['volume'],name="成交量",marker_color="blue",opacity=0.5,yaxis="y2"))

    fig2.update_layout(
        height=800,
        yaxis={'domain': [0.35, 1]} ,
        yaxis2={'domain': [0.15, 0.3]} ,
        title=f"{stockid}週線圖",
        
    )


    # fig2.update_xaxes(rangebreaks=[{"values": df_breaks}],showspikes=True,spikecolor="gray",spikethickness=1,spikesnap="cursor",spikemode="across",spikedash="solid")
    fig2.update_xaxes(showspikes=True,spikecolor="gray",spikethickness=1,spikesnap="cursor",spikemode="across",spikedash="solid")
    fig2.update_yaxes(showspikes=True,spikecolor="gray",spikethickness=1,spikesnap="cursor",spikemode="across",spikedash="solid")


    fig2.show()
    return fig2




