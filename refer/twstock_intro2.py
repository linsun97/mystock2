# stock — 股票歷史資訊
# stock 包含三個重要的元素： DATATUPLE 負責建立歷史股票資料之 namedtuple、 BaseFetcher 作為 TWSEFetcher 以及 TPEXFetcher 之基底 class、 Stock 封裝整個歷史股票資訊供使用者使用，同時 Stock 會針對上市或上櫃的股票代號 自動給予正確的 fetcher。

# DATATUPLE
# class stock.DATATUPLE(date, capacity, turnover, open, high, low, close, change, transaction)
# 歷史資料之 nametuple。

# Attributes:

# date
# datetime.datetime 格式之時間，例如 datetime.datetime(2017, 6, 12, 0, 0)。

# capacity
# 總成交股數 (單位: 股)。

# turnover
# 總成交金額 (單位: 新台幣/元)。

# open
# 開盤價。

# high
# 盤中最高價

# low
# 盤中最低價。

# close
# 收盤價。

# change
# 漲跌價差。

# transaction
# 成交筆數。

# Stock
# class stock.Stock(sid: str, initial_fetch: bool=True)
# 有關股票歷史資訊 (開/收盤價，交易量，日期…etc) 以及簡易股票分析。 建立 Stock 實例時，若 initial_fetch 為 True (預設)， 會自動呼叫 fetch_31() 抓取近 31 日之歷史股票資料。

# Class attributes are:

# sid
# 股票代號。

# fetcher
# 抓取方式之 instance，程式會自動判斷上櫃或上市，使用相對應之 fetcher。

# raw_data
# 經由 TWSEFetcher 或是 TPEXFetcher 抓取之原始資料。

# data
# 將 raw_data 透過 DATATUPLE 處理之歷史股票資料。

# Fetcher method:

# fetch(self, year: int, month: int)
# 擷取該年、月份之歷史股票資料。

# fetch_from(self, year: int, month: int)
# 擷取自該年、月至今日之歷史股票資料。

# fetch_31(self)
# 擷取近 31 日開盤之歷史股票資料。

# 分析 method:

# continuous(self, data)
# data 之持續上升天數。

# moving_average(self, data: list, days: int)
# data 之 days 日均數值。

# ma_bias_ratio(self, day1, day2)
# 計算 day1 日以及 day2 之乖離值。

# ma_bias_ratio_pivot(self, data, sample_size=5, position=False)
# 判斷正負乖離。

# Fetcher
# class stock.BaseFetcher
# fetch(self, year, month, sid, retry)
# 抓取相對應年月份之股票資料。

# _convert_date(self, date)
# 回傳西元記年，將民國記年轉換為西元記年。舉例而言:

# >>> date = self._convert_date('106/05/01')
# >>> print(date)
# '2017/05/01'
# _make_datatuple(self, data)
# 將相對應之單日資料轉換為 DATATUPLE。會將對應之資料轉換為對應型態。

# purify(self, original_data: list)
# 將 original_data 內之所有資料轉換為 DATATUPLE 型態。

# class stock.TWSEFetcher(BaseFetcher)
# 台灣上市股票抓取

# class stock.TPEXFetcher(BaseFetcher)
# 台灣上櫃股票抓取