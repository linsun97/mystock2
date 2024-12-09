from flask import Flask, render_template, url_for, flash, redirect , request , send_from_directory
from forms import filter_stocks, InputId , add_watch
from show_filt import Showfil
from tifrs_basic import get_cashgood,engine
import pandas as pd
import mariadb
from rci_kwr import get_allro
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import threading
import asyncio
import tkinter as tk
import matplotlib
import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader
from my_realtime_stock import get_shin_newhigh
from get_stockup import get_stockup
from get_stockum import get_stockum
from datetime import datetime
from pic_k import pic_k
from pic_k_w import pic_k_w
matplotlib.use('Agg')  # 強制使用 Agg 後端


app = Flask(__name__, static_folder="refer")
app.config['SECRET_KEY'] = 'my name is linsun'
app.config["DEBUG"] = True

yearnum = datetime.today().strftime('%Y')
t_year = int(yearnum) - 1911


@app.route("/")
def index():
    df_shin = pd.read_sql_query("select * from shin_oneday order by Up_date desc limit 1",engine)
    day1 = df_shin['day1_high'].values[0].split(",")
    d1v = df_shin['d1vo_high'].values[0].split(",")
    df_sup = pd.read_sql_query("select * from sup_oneday order by Up_date desc limit 1",engine)
    supday1 = df_sup['day1_high'].values[0].split(",")
    supd1v = df_sup['d1vo_high'].values[0].split(",")
    df_sum = pd.read_sql_query("select * from sum_oneday order by Up_date desc limit 1",engine)
    sumday1 = df_sum['day1_high'].values[0].split(",")
    # 抓出營收成長達標的股票做成的list
    monincome = pd.read_sql_query("select allstockid from monincome order by Up_date desc limit 1",engine)
    monid = monincome['allstockid'].values[0].split(",")
    # 抓出大戶比例增加的股票做成的list
    big_i = pd.read_sql_query("select stockid from big_increase ",engine)
    big_increase = big_i['stockid'].values[0].split(",")
    # 抓出投資現金與毛利率符合標準者
    good_s = pd.read_sql_query("select stockid from goodstocks ",engine)
    good_stocks = good_s['stockid'].tolist()
    # 將good_stocks內數字轉成字串
    good_stocks = list(map(str, good_stocks))
    # 抓出監控股
    def get_stocks():
        df_moni = pd.read_sql_query("select * from moniter",engine)
        id_list = df_moni['stockid'].tolist()
        name_list = df_moni['stockname'].tolist()
        return id_list,name_list
    # # 从数据表中获取五个值
    ids, names = get_stocks()
    idnum = len(ids)

    ra = get_allro("shin_oneday")
    ra_sup = get_allro("sup_oneday")
    try:
        db = mariadb.connect(
        host="localhost",
        user="root",
        password="nineseve9173",
        database="stock"
        )
        cursor = db.cursor()
        values1 = ", ".join([str(id) for id in day1])
        supvalues1 = ", ".join([str(id) for id in supday1])
        sumvalues1 = ", ".join([str(id) for id in sumday1])
        # 抓出stock_id有在day1的list做成的字串中的股票
        sql ="SELECT stockid,stockname FROM all_id_name_shin WHERE stockid IN (%s)"
        sq2 ="SELECT stockid,stockname FROM all_id_name WHERE stockid IN (%s)"
        sq3 ="SELECT stockid,stockname FROM all_id_name_sum WHERE stockid IN (%s)"
        try: 
            cursor.execute(sql % values1)
            results1 = cursor.fetchall()
        except Exception as e:
            print(e)
            results1 = [('1260','富味香')]
        try:
            cursor.execute(sq2 % supvalues1)
            results4 = cursor.fetchall()
        except Exception as e:
            print(e)
            results7 = [('1240','茂生農')]
        try:
            cursor.execute(sq3 % sumvalues1) 
            results7 = cursor.fetchall()
        except Exception as e:
            print(e)
            results7 = [('8487','愛爾達')]
        db.commit()
        db.close()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    return render_template('index.html',results1=results1,d1v=d1v,ra=ra,results4=results4,supd1v=supd1v,results7=results7,ra_sup=ra_sup,monid=monid,big_increase=big_increase,t_year=t_year,good_stocks=good_stocks,ids=ids,names=names,idnum=idnum,enumerate=enumerate,range=range)

@app.route("/goodstocks")
def goodstocks():
    cash_good = get_cashgood()
    # cash_good = cash_good.to_dict()
    # print(cash_good)
    return render_template('goodstocks.html',data=cash_good , enumerate=enumerate)

@app.route("/pic_stock" , methods=['GET', 'POST'])
def pic_stock():
    thread = threading.Thread()
    thread.start()
    form = InputId()
    if form.validate_on_submit():
        stockid = form.stockid.data
    else:
        stockid = request.args.get('stockid')
    # 使用 Pandas 繪製圖表
    # sql_query = f"""
    # SELECT * from st_{stockid}
    # LEFT JOIN big_index
    # ON st_{stockid}.up_date = big_index.Up_date 
    # ORDER BY st_{stockid}.up_date DESC limit 120;
    # """
    
    sql_query = f"SELECT * from st_{stockid} ORDER BY up_date DESC limit 120;"
    sql_query_b= f"SELECT * from big_index ORDER BY Up_date DESC limit 120;"
    sql_query_t = f"SELECT * from tpex_index ORDER BY Up_date DESC limit 120;"
    try:
        df1 = pd.read_sql_query(sql_query,engine)
        stockname = df1['stockname'].values[0]
        df = df1.iloc[::-1]
        # df['nh_num'] = df['nh'].apply(lambda x: len(x))
        # df['nh_num'] = df['nh'].str.len()
    except Exception as e:
        # print(e)
        return render_template('error.html',e=e)
    
    fig1, ax1 = plt.subplots()
    df.plot(kind='line', x='up_date',y='over', ax=ax1 ,figsize=(10, 2) ,color="red" ,legend=True)
    ax1.legend(loc='upper left')  # 設置圖例位置為左上角
    
  
    df_b = pd.read_sql_query(sql_query_b,engine)
    df_b = df_b.iloc[::-1]
    fig2, ax2 = plt.subplots()
    df_b.plot(kind='line', x='Up_date',y='Big', ax=ax2 ,figsize=(10, 2) ,color="green" ,legend=True)
    ax2.legend(loc='upper left')  # 設置圖例位置為左上角

    df_t = pd.read_sql_query(sql_query_t,engine)
    df_t = df_t.iloc[::-1]
    fig3, ax3 = plt.subplots()
    df_t.plot(kind='line', x='Up_date',y='Tpex', ax=ax3 ,figsize=(10, 2) ,color="blue",legend=True)
    ax3.legend(loc='upper left')  # 設置圖例位置為左上角

    sql_query_r = f"""
    SELECT * from st_{stockid}
    LEFT JOIN tpex_index
    ON st_{stockid}.up_date = tpex_index.Up_date 
    ORDER BY st_{stockid}.up_date DESC limit 120;
    """
    df_r = pd.read_sql_query(sql_query_r,engine)
    df_r = df_r.iloc[::-1]
    df_r['r'] = df_r['over']/df_r['Tpex']
    x = df_r['r'].values[0]
    df_r['r_r'] = df_r['r']/x
    fig4, ax4 = plt.subplots()
    df_r.plot(kind='line', x='Up_date',y='r_r', ax=ax4 ,figsize=(10, 2) ,color="blue" ,ylabel="Tpex/over--ration" ,legend=True )
    ax4.legend(loc='upper left')  # 設置圖例位置為左上角

    # 將圖表保存為圖片文件
    img1 = BytesIO()
    fig1.savefig(img1, format='png')
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode('utf8')
    img2 = BytesIO()
    fig2.savefig(img2, format='png')
    img2.seek(0)
    plot_url2 = base64.b64encode(img2.getvalue()).decode('utf8')
    img3 = BytesIO()
    fig3.savefig(img3, format='png')
    img3.seek(0)
    plot_url3 = base64.b64encode(img3.getvalue()).decode('utf8')
    img4 = BytesIO()
    fig4.savefig(img4, format='png')
    img4.seek(0)
    plot_url4 = base64.b64encode(img4.getvalue()).decode('utf8')
    
    return render_template('pic_stock.html', stockid=stockid, stockname=stockname, plot_url1=plot_url1, plot_url2=plot_url2, plot_url3=plot_url3, plot_url4=plot_url4 , df1=df1,df_b=df_b,df_t=df_t,df_r=df_r,t_year=t_year)

@app.route("/tpexvsnum")
def tpexvsnum():
    thread = threading.Thread()
    thread.start()

    sql1 = "SELECT * FROM sup_oneday LEFT JOIN tpex_index ON sup_oneday.Up_date = tpex_index.Up_date order by sup_oneday.Up_date ;"
    df = pd.read_sql_query(sql1,engine)
    df['day1_num'] = df['day1_high'].apply(lambda x: len(x))
    # df['Up_date']應該是 2024-05-01 12:12:00 這種格式
    df['update'] = df['Up_date'].iloc[:,0]
    # 繪製折線圖
    fig1, ax1 = plt.subplots()
    df.plot(kind='line',x='update',y='Tpex', ax=ax1 ,figsize=(12, 3) ,color="green" )
    # # 繪製直方圖
    
    fig2, ax2 = plt.subplots()
    df.plot(kind='bar', x='update',y='day1_num', ax=ax2 ,figsize=(12, 3) ,color="red")
    
    img1 = BytesIO()
    fig1.savefig(img1, format='png')
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode('utf8')
    img2 = BytesIO()
    fig2.savefig(img2, format='png')
    img2.seek(0)
    plot_url2 = base64.b64encode(img2.getvalue()).decode('utf8')

    # return render_template('tpexvsnum.html',plot_url1=plot_url1,plot_url2=plot_url2)
    return render_template('tpexvsnum.html',plot_url1=plot_url1,plot_url2=plot_url2)

@app.route("/shin_high")
def shin_high():
    high1,high2,high3,hvol1 = get_shin_newhigh()
    monincome = pd.read_sql_query("select allstockid from monincome order by Up_date desc limit 1",engine)
    monid = monincome['allstockid'].values[0].split(",")
    big_i = pd.read_sql_query("select stockid from big_increase ",engine)
    big_increase = big_i['stockid'].values[0].split(",")
     # 抓出投資現金與毛利率符合標準者
    good_s = pd.read_sql_query("select stockid from goodstocks ",engine)
    good_stocks = good_s['stockid'].tolist()
    # df = get_shin_newhigh()
    return render_template('shin_high.html',high1=high1,high2=high2,high3=high3,hvol1=hvol1,monid=monid,big_increase=big_increase,t_year=t_year,good_stocks=good_stocks)
    # return render_template('shin_high.html',df=df)

@app.route("/sup_high")
def sup_high():
    high1,high2,high3,hvol1 = get_stockup()
    monincome = pd.read_sql_query("select allstockid from monincome order by Up_date desc limit 1",engine)
    monid = monincome['allstockid'].values[0].split(",")
    big_i = pd.read_sql_query("select stockid from big_increase ",engine)
    big_increase = big_i['stockid'].values[0].split(",")
     # 抓出投資現金與毛利率符合標準者
    good_s = pd.read_sql_query("select stockid from goodstocks ",engine)
    good_stocks = good_s['stockid'].tolist()
    # df = get_shin_newhigh()
    return render_template('sup_high.html',high1=high1,high2=high2,high3=high3,hvol1=hvol1,monid=monid,big_increase=big_increase,t_year=t_year,good_stocks=good_stocks)

@app.route("/sum_high")
def sum_high():
    high1,high2,high3,hvol1 = get_stockum()
    monincome = pd.read_sql_query("select allstockid from monincome order by Up_date desc limit 1",engine)
    monid = monincome['allstockid'].values[0].split(",")
    big_i = pd.read_sql_query("select stockid from big_increase ",engine)
    big_increase = big_i['stockid'].values[0].split(",")
     # 抓出投資現金與毛利率符合標準者
    good_s = pd.read_sql_query("select stockid from goodstocks ",engine)
    good_stocks = good_s['stockid'].tolist()
    # df = get_shin_newhigh()
    return render_template('sum_high.html',high1=high1,high2=high2,high3=high3,hvol1=hvol1,monid=monid,big_increase=big_increase,t_year=t_year,good_stocks=good_stocks)

@app.route("/pic_k_page")
def pic_k_page():
    stockid = request.args.get('stockid')
    fig1 = pic_k(stockid)
    # fig1.write_html('templates/chart.html')
    return render_template('pic_k_page.html',stockid = stockid)

@app.route("/pic_wk_page")
def pic_wk_page():
    stockid = request.args.get('stockid')
    fig1 = pic_k_w(stockid)
    # fig1.write_html('templates/chart1.html')
    return render_template('pic_wk_page.html',stockid = stockid)

@app.route("/add_wh", methods=['GET', 'POST'])
def add_wh():
    def get_stocks():
        df_moni = pd.read_sql_query("select * from moniter",engine)
        id_list = df_moni['stockid'].tolist()
        name_list = df_moni['stockname'].tolist()
        return id_list,name_list
    # # 从数据表中获取五个值
    ids, names = get_stocks()
    idnum = len(ids)

    # if request.method == 'POST':
    #     stockid_list =[]
    #     stockname_list =[]
    #     for i in range(idnum+10):
    #         if request.args.get(f'stockid{i}') :
    #             stockid_list.append(request.args.get(f'stockid{i}'))
    #             stockname_list.append(request.args.get(f'stockname{i}'))
    #     df_add = pd.DataFrame({'stockid':stockid_list,'stockname':stockname_list})
    #     df_add.to_sql('moniter',engine,if_exists='replace',index=False)
                
    return render_template('add_watch.html',enumerate=enumerate,ids=ids,names=names,idnum=idnum)

@app.route("/success", methods=['GET', 'POST'])
def success():
    def get_stocks():
        df_moni = pd.read_sql_query("select * from moniter",engine)
        id_list = df_moni['stockid'].tolist()
        name_list = df_moni['stockname'].tolist()
        return id_list,name_list
    # # 从数据表中获取五个值
    ids, names = get_stocks()
    idnum = len(ids)

    stockid_list =[]
    stockname_list =[]
    # aa = request.args.get('stockid0')
    for i in range(idnum+10):
        if request.args.get(f'stockid{i}') :
            stockid_list.append(request.args.get(f'stockid{i}'))
            stockname_list.append(request.args.get(f'stockname{i}'))
    df_add = pd.DataFrame({'stockid':stockid_list,'stockname':stockname_list})
    df_add.to_sql('moniter',engine,if_exists='replace',index=False)
    flash('成功新增股票')
    return render_template('success.html',stockid_list=stockid_list,stockname_list=stockname_list,enumerate=enumerate)

@app.route("/home")
def home():
    show_df , td_num  = Showfil()
    return render_template('home.html',show_df=show_df , td_num=td_num)

@app.route("/newup")
def newup():
    return render_template('file_list_sorted.html')

@app.route("/moni")
def moni():
    return render_template('file_list_moni.html')

@app.route("/goods")
def goods():
    return render_template('file_list_goods.html')

@app.route("/refer/report_new")
def serve_static(filename):
    # 提供 refer 資料夾下的檔案
    return send_from_directory("refer", filename)

@app.route("/filter", methods=['GET', 'POST'])
def filter():
    form = filter_stocks()
    if form.validate_on_submit():
        # 現金流量
        cash_check = form.cash_check.data
        cash_a = form.cash_a.data
        # 千張以上大戶比例
        bigguy_check = form.bigguy_check.data
        bigguy_a = form.bigguy_a.data
        # 資本額限制
        capital_check = form.capital_check.data
        capital_a = form.capital_a.data
        # 公司成立不超過幾年
        estab_check = form.estab_check.data
        estab_a = form.estab_a.data
        # 公司掛牌不超過幾年
        up_check = form.up_check.data
        up_a = form.up_a.data
        # 毛利率不低於多少
        netrate_check = form.netrate_check.data
        netrate_a = form.netrate_a.data
        # 淨利率不低於多少
        oprate_check = form.oprate_check.data
        oprate_a = form.oprate_a.data
        # 成交價創n日新高
        price_check = form.price_check.data
        price_a = form.price_a.data
        # 成交量創n日新高
        amount_check = form.amount_check.data
        amount_a = form.amount_a.data

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('filter'))
    return render_template('filter.html', title='Filter', form=form)


# @app.route("/login", methods=['GET', 'POST'])
# def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     if form.email.data == 'admin@blog.com' and form.password.data == 'password':
    #         flash('You have been logged in!', 'success')
    #         return redirect(url_for('filter'))
    #     else:
    #         flash('Login Unsuccessful. Please check username and password', 'danger')
    # return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)