from flask import Flask, render_template, url_for, flash, redirect , request
from forms import filter_stocks, LoginForm
from show_filt import Showfil
from tifrs_basic import get_cashgood,engine
import pandas as pd
import mariadb
from rci_kwr import get_allro
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import threading
from celery import Celery

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config["DEBUG"] = True




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

    return render_template('index.html',results1=results1,d1v=d1v,ra=ra,results4=results4,supd1v=supd1v,results7=results7,ra_sup=ra_sup,monid=monid,enumerate=enumerate)

@app.route("/goodstocks")
def goodstocks():
    cash_good = get_cashgood()
    # cash_good = cash_good.to_dict()
    # print(cash_good)
    return render_template('goodstocks.html',data=cash_good , enumerate=enumerate)

@app.route("/pic_stock")
def pic_stock():
    stockid = request.args.get('stockid')
    # 使用 Pandas 繪製圖表
    sql_query = f"""
    SELECT * from st_{stockid}
    LEFT JOIN big_index
    ON st_{stockid}.up_date = big_index.Up_date 
    ORDER BY st_{stockid}.up_date DESC limit 120;
    """
    df = pd.read_sql_query(sql_query,engine)
    df = df.iloc[::-1]
    fig1, ax1 = plt.subplots()
    df.plot(kind='line', x='up_date',y='Big', ax=ax1 ,figsize=(10, 6) ,color="red")
    fig2, ax2 = plt.subplots()
    df.plot(kind='line', x='up_date',y='over', ax=ax2 ,figsize=(10, 6) )
    # plt.switch_backend('agg')
    # plt.title('Two Lines in One Plot')
    # plt.xlabel('Index')
    # plt.ylabel('Value')
    # plt.show()
    # 將圖表保存為圖片文件
    img1 = BytesIO()
    fig1.savefig(img1, format='png')
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode('utf8')
    img2 = BytesIO()
    fig2.savefig(img2, format='png')
    img2.seek(0)
    plot_url2 = base64.b64encode(img2.getvalue()).decode('utf8')
    plt.close('all')
    return render_template('pic_stock.html', stockid=stockid, plot_url1=plot_url1, plot_url2=plot_url2)

@app.route("/home")
def home():
    show_df , td_num  = Showfil()
    return render_template('home.html',show_df=show_df , td_num=td_num)

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


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    #     if form.email.data == 'admin@blog.com' and form.password.data == 'password':
    #         flash('You have been logged in!', 'success')
    #         return redirect(url_for('filter'))
    #     else:
    #         flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)