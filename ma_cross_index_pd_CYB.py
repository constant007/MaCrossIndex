#适用于优矿
#MA短周期和长周期金叉的交易策略
import math
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from datetime import timedelta,date

start = '20120101'                       # 回测起始时间
end =   '20151210'                         # 回测结束时间
benchmark = '399006.ZICN'  # 策略参考标准
universe = ['159915.XSHE']  # 证券池，支持股票和基金 

capital_base = 100000                      # 起始资金
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

#self defined data
#最优参数，ma_short=8 ma_long=26;当开盘MA8和MA26金叉时买入，MA8和MA26死叉时卖出
#short(8 9 10 11)  long(25 26 27 28)
window_short = 8
window_long = 26
universe_tuple = tuple(universe)

def initialize(account):                   # 初始化虚拟账户状态
    pass

def handle_data(account):                  # 每个交易日的买入卖出指令
    hist = account.get_attribute_history('closePrice',window_long)
    fund = universe_tuple[0]
    today = account.current_date
    preday100 = today + timedelta(days = -100)
    yestoday = today + timedelta(days = -100)
    
    #yestoday 使用today会使用未来数据；更改这个后，maIndexShort.values[-1]可以使用；
    cIndex = DataAPI.MktIdxdGet(ticker='399006',beginDate=preday100,endDate=yestoday,field=["tradeDate","closeIndex"],pandas="1")
    
    maIndexShort  = np.round(pd.rolling_mean(cIndex['closeIndex'],window=window_short),2)
    maIndexLong  = np.round(pd.rolling_mean(cIndex['closeIndex'],window=window_long),2)
    
    #maIndexShort.values[-1] 就会使用未来的数据 （不再有效）
    if maIndexShort.values[-1]>= maIndexLong.values[-1]:
        if account.position.secpos.get(fund, 0) == 0:
            # *1.02 为了防跳空高开，买不到那么多的头寸
            approximationAmount = int(account.cash/(hist[universe_tuple[0]][-1]*1.02)/100.0) * 100
            order(universe_tuple[0],approximationAmount)
    elif maIndexShort.values[-1] < maIndexLong.values[-1]:
        if account.position.secpos.get(fund, 0) > 0:
            order_to(universe_tuple[0],0)
    else :
        if isnan(maIndexShort.values[-1]) or isnan(maIndexLong.values[-1]) :
            print 'Warning : MA is NaN.'
        pass
    

#for parameter opt
print 'windowLong windowShort  annualized_return     sharpe    max_drawdown'
for window_long in range(15,70,1):
    for window_short in range(1,15,1):
        sim_params = quartz.sim_condition.env.SimulationParameters(start, end, benchmark, universe, capital_base)
        strategy = quartz.sim_condition.strategy.TradingStrategy(initialize, handle_data) 
        idxmap_all, data_all = quartz.sim_condition.data_generator.get_daily_data(sim_params)
        bt_test, acct = quartz.quick_backtest(sim_params, strategy, idxmap_all, data_all)
        perf = quartz.perf_parse(bt_test, acct)
        print '{0:2d}    {1:2d}          {2:>7.4}%           {3:>7.4}      {4:>7.4}'.format(window_long,window_short,perf['annualized_return']*100, perf['sharpe'], perf['max_drawdown'])
