'''
Created on Apr 6, 2019

@author: ben
'''
from zipline.api import record, symbol, order_target_percent #@UnresolvedImport
from zipline import run_algorithm
from datetime import datetime
import pytz
import matplotlib.pyplot as plt

base_capital = 10000
start = datetime(2000, 1, 1, 0, 0, 0, 0, pytz.utc)
end = datetime(2010, 1, 1, 0, 0, 0, 0, pytz.utc)


def initialize(context):
    context.amzn = symbol('AMZN')


def handle_data(context, data):

    long_mavg = data.history(context.amzn, 'close', 41, '1d')[:-1].mean()
    short_mavg = data.history(context.amzn, 'close', 21, '1d')[:-1].mean()


    if short_mavg > long_mavg:
        if data.can_trade(context.amzn):
            order_target_percent(context.amzn, 1.00)
   
    else:
        if data.can_trade(context.amzn):
            order_target_percent(context.amzn, -1.00)
    
    record(AMZN=data[context.amzn].price)        
    record(long_mavg=long_mavg)
    record(short_mavg=short_mavg)



perf = run_algorithm(start, end, initialize, base_capital, handle_data,
        bundle = 'quantopian-quandl')

perf.to_csv('tearsheet.csv')
plt.figure()
perf.portfolio_value.plot(label="Portfolio value")

plt.legend()
plt.savefig('returns.png')

plt.figure()
perf.AMZN.plot(label='AMZN')
perf.long_mavg.plot(label='Long Moving Average')
perf.short_mavg.plot(label='Short Moving Average')

plt.legend()
plt.savefig('amzn.png')
plt.show()




