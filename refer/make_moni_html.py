import os
from datetime import datetime

# 指定資料夾名稱
folder_name = "report_moniter"
output_file = "../templates/file_list_moni.html"

# 獲取資料夾中所有檔案名稱
file_list = os.listdir(folder_name)

# 過濾出以 .html 為副檔名的檔案並提取日期
html_files = [file for file in file_list if file.endswith(".html")]

# 建立字典以儲存年份和月份分類
file_dict = {}

for file in html_files:
    try:
        # 提取日期部分 (假設檔名格式為 YYYYMMDD_*)
        date_str = file.split('_')[0]
        file_date = datetime.strptime(date_str, "%Y%m%d")
        year = file_date.year
        month = file_date.month
        
        # 初始化分類結構
        if year not in file_dict:
            file_dict[year] = {}
        if month not in file_dict[year]:
            file_dict[year][month] = []
        
        # 加入對應的年份和月份清單
        file_dict[year][month].append((file_date, file))
    except ValueError:
        # 若檔名格式不符合，跳過該檔案
        print(f"跳過無效檔案: {file}")

# 將檔案按日期排序 (最近的在最前面)
for year in file_dict:
    for month in file_dict[year]:
        file_dict[year][month].sort(reverse=True, key=lambda x: x[0])

# 開始生成 HTML 檔案
with open(output_file, "w", encoding="utf-8") as f:
    # 寫入 HTML 頭部資訊
    f.write("<!DOCTYPE html>\n")
    f.write("<html lang='zh-TW'>\n")
    f.write("<head>\n")
    f.write("<meta charset='UTF-8'>\n")
    f.write("<title>分類檔案清單</title>\n")
    f.write("<style>\n")
    f.write("table { width: 100%; border-collapse: collapse; }\n")
    f.write("td, th { border: 1px solid #ddd; padding: 8px; vertical-align: top; }\n")
    f.write("th { background-color: #f2f2f2; }\n")
    f.write("</style>\n")
    f.write("</head>\n")
    f.write("<body>\n")
    f.write("<h1>分類檔案清單</h1>\n")
    
    # 生成分類的檔案清單
    for year in sorted(file_dict.keys(), reverse=True):  # 年份由新到舊
        f.write(f"<h2>{year} 年</h2>\n")
        f.write("<table>\n")
        months = sorted(file_dict[year].keys(), reverse=True)  # 月份由新到舊
        
        # 每兩個月份分成一列
        for i in range(0, len(months), 2):
            f.write("<tr>\n")
            for j in range(2):  # 一列兩個月
                if i + j < len(months):
                    month = months[i + j]
                    f.write(f"<td><h3>{month} 月</h3>\n<ul>\n")
                    for file_date, file in file_dict[year][month]:
                        file_path = os.path.join(folder_name, file)
                        f.write(f"<li><a href='refer/{file_path}' target='_blank'>{file}</a> - {file_date.strftime('%Y-%m-%d')}</li>\n")
                    f.write("</ul></td>\n")
                else:
                    # 如果月份不足，填空白單元格
                    f.write("<td></td>\n")
            f.write("</tr>\n")
        
        f.write("</table>\n")
    
    f.write("</body>\n")
    f.write("</html>\n")

print(f"分類後的 HTML 檔案 '{output_file}' 已生成，請開啟檢視。")
