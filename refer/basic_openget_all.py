from basic_opengetall_def import Get_openbasic
from del_dbtable import DelDbTable
import time
from datetime import date

def runall():
    DelDbTable("stock","basic_open_all")
    for i in range(1,4):
        Get_openbasic(i)
        time.sleep(30)

today = date.today()
# print(today)
today_year = today.strftime("%Y")
# print(date(int(today_year), 4, 1))
# quit()
if today == date(int(today_year), 4, 1):
    runall()
elif today == date(int(today_year), 5, 20):
    runall()
elif today == date(int(today_year), 8, 20):  
    runall()
elif today == date(int(today_year), 11, 20):
    runall()




