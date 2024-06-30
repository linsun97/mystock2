import pandas as pd
import mariadb
from sqlalchemy import create_engine


engine = create_engine('mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock')
def get_allro(table):
    try:
            db = mariadb.connect(
            host="localhost",
            user="root",
            password="nineseve9173",
            database="stock"
            )
            cursor = db.cursor()
            df_shin = pd.read_sql_query(f"select * from {table} order by Up_date desc limit 1",engine)
            day1 = df_shin['day1_high'].values[0].split(",")
            df_id = pd.DataFrame(day1)
            ra = []
            def get_r(row):
                sql = f"SELECT rci,updown,kwr,rs from st_{row[0]} order by up_date desc limit 1"
                df_ra = pd.read_sql_query(sql,engine)
                print(df_ra)
                # quit()
                raone = [df_ra['rci'].values[0],df_ra['updown'].values[0],df_ra['kwr'].values[0],df_ra['rs'].values[0]]
                ra.append(raone)
                # cursor.execute(sql)
                # results = cursor.fetchall()
                # print(results)
                # ra.append(results)
                # quit()
            # print(df_id)
            df_id.apply(get_r,axis=1)
            return ra
    except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")