#适于优矿
#当ma_short 向上 且 ma_long向上时买入； ma_short 向下 ma_long向下卖出
import math
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from datetime import timedelta,date

start = '20120101'                       # 回测起始时间
end =   '20160111'                         # 回测结束时间
benchmark = 'HS300'                        # 策略参考标准
#benchmark = '399006.ZICN'
universe = ['159915.XSHE']  # 证券池，支持股票和基金 
#universe = ['510050.XSHG'] 
commission = Commission(0.0,0.0)



capital_base = 100000                      # 起始资金
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

#self defined data
#最优参数，ma_short=8 ma_long=26;当开盘MA3和MA23金叉时买入，MA3和MA23死叉时卖出

#(3 20) (5 21)
window_short = 3
window_long = 20
universe_tuple = tuple(universe)

#def getema(cIndex n):
#    k=2.0/(n+1)
#    ema=cIndex[0]
#    for(i=0;i<n;i++)
#        ema=cIndex[-1]*k+ema(1-k)
        

def initialize(account):                   # 初始化虚拟账户状态
    pass

def handle_data(account):                  # 每个交易日的买入卖出指令
    hist = account.get_attribute_history('closePrice',window_long)
    fund = universe_tuple[0]
    today = account.current_date
    preday = today + timedelta(days = -100)
    yestoday = today + timedelta(days = -1)


    cIndex = DataAPI.MktIdxdGet(ticker='399006',beginDate=preday,endDate=yestoday,field=["tradeDate","closeIndex"],pandas="1")
    maIndexShort  = np.round(pd.rolling_mean(cIndex['closeIndex'],window=window_short),2)
    maIndexLong  = np.round(pd.rolling_mean(cIndex['closeIndex'],window=window_long),2)
    filter_std = np.std(cIndex['closeIndex'][-window_long:],axis=0)  #not used

    if maIndexShort.values[-1] > maIndexShort.values[-2]  and maIndexLong.values[-1] > maIndexLong.values[-2] :
        if account.position.secpos.get(fund, 0) == 0:
            approximationAmount = int(account.cash / (hist[universe_tuple[0]][-1]*1.02)/100.0) * 100
            order(universe_tuple[0],approximationAmount)
    elif maIndexShort.values[-1] < maIndexShort.values[-2] and maIndexLong.values[-1] < maIndexLong.values[-2]  :
        if account.position.secpos.get(fund, 0) > 0:
            order_to(universe_tuple[0],0)
    else :
        #if isnan(maIndexShort.values[-1]) or isnan(maIndexLong.values[-1]) :
        #    print 'Warning : MA is NaN.'
        pass
