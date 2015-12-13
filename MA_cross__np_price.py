import numpy as np
import pandas as pd


start = '20120101'                       # 回测起始时间
end = '20151210'                         # 回测结束时间
benchmark = 'HS300'                        # 策略参考标准
#benchmark = '399006.ZICN'
universe = ['159915.XSHE']  # 证券池，支持股票和基金 


capital_base = 100000                      # 起始资金
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

#self defined data
#最优参数，ma_short=3 ma_long=23;当开盘MA3和MA23金叉时买入，MA3和MA23死叉时卖出
window_short = 8
window_long = 26
universe_tuple = tuple(universe)

def initialize(account):                   # 初始化虚拟账户状态
    pass

def handle_data(account):                  # 每个交易日的买入卖出指令
    hist = account.get_attribute_history('closePrice',window_long)
    fund = universe_tuple[0]
    today = account.current_date
    
    maShort =  np.mean(hist[universe_tuple[0]][-window_short:])
    maLong = np.mean(hist[universe_tuple[0]][-window_long:])
    
    flag = True if(maShort>= maLong) else False
    
    if flag:
        if account.position.secpos.get(fund, 0) == 0:
            approximationAmount = int(account.cash / (hist[universe_tuple[0]][-1]*1.02)/100.0) * 100
            order(universe_tuple[0],approximationAmount)
    else:
        if account.position.secpos.get(fund, 0) >= 0:
            order_to(universe_tuple[0],0)    

