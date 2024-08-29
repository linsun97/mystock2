import requests
import os
import zipfile
import pandas as pd
import os
import time
import requests
from tqdm import tqdm
from sqlalchemy import create_engine
from datetime import date

engine = create_engine("mariadb+mariadbconnector://root:nineseve9173@127.0.0.1:3306/stock")

today = date.today()
# print(today)
today_year = today.strftime("%Y")
# print(date(int(today_year), 4, 1))
# quit()
if today == date(int(today_year), 4, 1):
    upyear = str(int(today_year) - 1)
    season = "Q4"
    sen_no = 4
    inv_l = 2
elif today == date(int(today_year), 5, 20):
    upyear = str(today_year)
    season = "Q1"
    sen_no = 1
    inv_l = 1
elif today == date(int(today_year), 8, 20):  
    upyear = str(today_year)
    season = "Q2"
    sen_no = 2
    inv_l = 1.33
elif today == date(int(today_year), 11, 20):
    upyear = str(today_year)
    season = "Q3"
    sen_no = 3
    inv_l = 1.66
else:
    quit()
    # pass

# upyear = "2024"
# season = "Q1"
# inv_l = 1
# sen_no = 1

# 設定下載的 URL 和目標檔案路徑
url = f'https://mops.twse.com.tw/server-java/FileDownLoad?step=9&functionName=show_file2&fileName=tifrs-{upyear}{season}.zip&filePath=/ifrs/{upyear}/'
print(url)
target_folder = './'
target_file = os.path.join(target_folder, f'tifrs-{upyear}{season}.zip')

# # 下載檔案：使用 requests 庫下載檔案，並將其設為流（stream）模式，以便逐步下載。
response = requests.get(url,stream=True)
if response.status_code == 200:
    # 計算下載檔案的總大小
    total_size = int(response.headers.get('content-length', 0))
    print(f'檔案大小：{total_size} bytes')
    # 計算下載檔案的進度
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc='下載進度')

    # 下載檔案
    with open(target_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                progress_bar.update(len(chunk))

    # 顯示下載完成
    print(f'檔案下載完成！大小：{total_size} bytes')
else:
    print(f'下載失敗：{response.status_code}')

# quit()
pd.set_option("display.max_columns", 500)
file = zipfile.ZipFile(f'tifrs-{upyear}{season}.zip', 'r')
# file = zipfile.ZipFile(f'tifrs-2024Q1.zip', 'r')
# print(file.namelist())
# quit()
# # "https://mops.twse.com.tw/server-java/FileDownLoad?step=9&functionName=show_file2&fileName=tifrs-2024Q4.zip&filePath=/ifrs/2024/"

ids = []
caps = []
net_rs = []
inv_caps = []
for name in file.namelist():
    # print(name)
    # dirfile = name.split("/")[1]
    # filename = dirfile.split(".")[0]
    filename = name.split(".")[0]
    # print(filename)
    id = filename.split("-")[5]
    up_date = filename.split("-")[6]
    # print(id)
    # print(up_date)
    # quit()
    if len(id) == 4 :
        df = pd.read_html(file.open(name))
        # print(df)
        # quit()
        # print(df[0].shape)
        # quit()
        df[0].columns = [chr(i) for i in range(97, 97 + len(df[0].columns))]
        # print(df[0].columns)
        # quit()
        # df[0].columns = ["a","b","c","d","e"]
        # print(df[0])
        # 找出股本
        if "3110" in df[0]['a'].values:
            captial = df[0].loc[df[0]['a'] == "3110","c"].values[0]
        else:
            if 301010.0 in df[0]['a'].values:
                captial = df[0].loc[df[0]['a'] == 301010.0,"c"].values[0]
            else:
                if "31100" in df[0]['a'].values:
                    captial = df[0].loc[df[0]['a'] == "31100","c"].values[0]
                else:
                    captial = 1
        # captial = df[0].loc[df[0]['a'] == "3110","c"].values[0]
        if captial == "NaN":
            captial = 0
        # 將股本轉為"億"
        captial = int(captial)
        cap = round(captial/100000,2)
        # print(cap)
        # print(df[1])

        # ---------------------------------------
        # print(df[1].shape)
        df[1].columns = [chr(i) for i in range(97, 97 + len(df[1].columns))]
        # df[1].columns = ["a","b","c","d"]
        # print(df[1])
        # quit()
        # 找出營業收入,營業毛利
        if 4000.0 in df[1]['a'].values:
            income = df[1].loc[df[1]['a'] == 4000.0,"c"].values[0]
        else:
            income = 0
        if 4000 in df[1]['a'].values:
            income = df[1].loc[df[1]['a'] == 4000,"c"].values[0]
        else:
            income = 0

        # print(income)
        # income = df[1].loc[df[1]['a'] == 4000.0,"c"].values[0]
        # print(income)
        if 5900.0 in df[1]['a'].values:
            netincome = df[1].loc[df[1]['a'] == 5900.0,"c"].values[0]
        else:
            if 5900 in df[1]['a'].values:
                netincome = df[1].loc[df[1]['a'] == 5900,"c"].values[0]
            else:
                netincome = 0
                
        # netincome = df[1].loc[df[1]['a'] == 5900.0,"c"].values[0]
        # print(netincome)
        if "(" in str(income):
            # print("營業收入為負號")
            income = 0
            # print(income)
        if "(" in str(netincome):
            # print("營業毛利為負號")
            netincome = 0
            # print(netincome)
        # 算出營業毛利率
        if int(income) == 0 or int(netincome) == 0:
            net_r = 0
        else:
            net_r = round((float(netincome)/float(income))*100,2)
        # print(net_r)
        # print(df[1])

        # ---------------------------------------

        # print(df[2].shape)
        df[2].columns = [chr(i) for i in range(97, 97 + len(df[2].columns))]
        # df[2].columns = ["a","b","c","d"]
        # print(df[2].head(10))
        # quit()
        # 找出營業收入,營業毛利
        if "B02700" in df[2]['a'].values:
            invest = df[2].loc[df[2]['a'] == "B02700","c"].values[0]
        else:
            invest = 0
        # invest = df[2].loc[df[2]['a'] == "B02700","c"].values[0]
        # print(invest)
        if "(" in str(invest):
            # print("有負號")
            invest = invest.replace('(','')
            invest = invest.replace(')','')
            invest = invest.replace(',','')
            # print(invest)
            invest = int(invest)/100000
            # print(invest)
        else:
            invest = 0
            # print(invest)

        inv_cap = round(invest/cap,2)
        # print(inv_cap)

        # ---------------------------------------
        # print("id:",id,"  cap:",cap,"  net_r:",net_r,"  inv_cap:",inv_cap)
        
        
        if (inv_cap >= inv_l) and (net_r >= 30):
            print("符合條件")
            ids.append(id)
            caps.append(cap)
            net_rs.append(net_r)
            inv_caps.append(inv_cap)

file.close()            

goodstocks = {
                "stockid":ids,
                "capital":caps,
                "net_r" : net_rs,
                "inv_cap":inv_caps
            }

# print(goodstocks)
df_goodstocks = pd.DataFrame(goodstocks,columns=["stockid","capital","net_r","inv_cap"])
df_goodstocks['upyear'] = upyear
df_goodstocks['season'] = sen_no 
df_goodstocks=df_goodstocks.sort_values(by=['inv_cap'], ascending=False)
df_goodstocks =df_goodstocks.astype(
    {"stockid": "int16",
     "capital": "float32",
     "net_r": "float32",
     "inv_cap": "float32",
     "upyear": "int16",
     "season": "int16"
        })
df_goodstocks.to_sql('goodstocks', engine, if_exists='append', index=False)
# print(df_goodstocks)


# Specify the path to the zip file
# Delete the zip file
zip_file_path = f'tifrs-{upyear}{season}.zip'
if os.path.exists(zip_file_path):
    os.remove(zip_file_path)
    print(f"檔案 '{zip_file_path}' 已成功刪除。")
else:
    print(f"檔案 '{zip_file_path}' 不存在。")


