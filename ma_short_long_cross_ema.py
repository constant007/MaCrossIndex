#适用于优矿
#EXPMA交叉的策略，但是没有比较好的参数
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
#(8 9 10 11) (25 26 27 28)
window_short = 3
window_long = 26

universe_tuple = tuple(universe)

def initialize(account):                   # 初始化虚拟账户状态
    pass

def handle_data(account):                  # 每个交易日的买入卖出指令
    hist = account.get_attribute_history('closePrice',window_long)
    fund = universe_tuple[0]
    today = account.current_date
    preday = today + timedelta(days = -300)  #！参数必须大于200，否则EMA计算的值不准确；
    yestoday = today + timedelta(days = -1)
    
    cIndex = DataAPI.MktIdxdGet(ticker='399006',beginDate=preday,endDate=yestoday,field=["tradeDate","closeIndex"],pandas="1")
    maIndexShort  = np.round(pd.rolling_mean(cIndex['closeIndex'],window=window_short),2)
    maIndexLong  = np.round(pd.rolling_mean(cIndex['closeIndex'],window=window_long),2)
    ema_short = pd.ewma(cIndex.closeIndex, span=window_short)
    ema_long = pd.ewma(cIndex.closeIndex, span=window_long)
    filter_std = np.std(cIndex['closeIndex'][-window_long:],axis=0)

    if ema_short.values[-1] >= ema_long.values[-1] :
        if account.position.secpos.get(fund, 0) == 0:
            approximationAmount = int(account.cash / (hist[universe_tuple[0]][-1]*1.02)/100.0) * 100
            order(universe_tuple[0],approximationAmount)
    elif ema_short.values[-1] < ema_long.values[-1] :
        if account.position.secpos.get(fund, 0) > 0:
            order_to(universe_tuple[0],0)
    else :
        pass

print 'window windows  annualized_return     sharpe    max_drawdown'
for window_long in range(19,70,1):
    for window_short in range(2,15,1):
        sim_params = quartz.sim_condition.env.SimulationParameters(start, end, benchmark, universe, capital_base)
        strategy = quartz.sim_condition.strategy.TradingStrategy(initialize, handle_data) 
        idxmap_all, data_all = quartz.sim_condition.data_generator.get_daily_data(sim_params)
        bt_test, acct = quartz.quick_backtest(sim_params, strategy, idxmap_all, data_all)
        perf = quartz.perf_parse(bt_test, acct)
        print '{0:2d}    {1:2d}          {2:>7.4}%           {3:>7.4}      {4:>7.4}'.format(window_long,window_short,perf['annualized_return']*100, perf['sharpe'], perf['max_drawdown'])
