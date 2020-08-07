from zipline.api import order_target, record, symbol #@UnresolvedImport
from zipline import run_algorithm
from datetime import datetime
import pytz
import matplotlib.pyplot as plt

base_capital = 10000
start = datetime(2000, 1, 1, 0, 0, 0, 0, pytz.utc)
end = datetime(2010, 1, 1, 0, 0, 0, 0, pytz.utc)

def initialize(context):
    context.i = 0
    context.asset = symbol('AAPL')


def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300:
        return

    # Compute averages
    # data.history() has to be called with the same params
    # from above and returns a pandas dataframe.
    short_mavg = data.history(context.asset, 'price', bar_count=100, frequency="1d").mean()
    long_mavg = data.history(context.asset, 'price', bar_count=300, frequency="1d").mean()

    # Trading logic
    if short_mavg > long_mavg:
        # order_target orders as many shares as needed to
        # achieve the desired number of shares.
        order_target(context.asset, 100)
    elif short_mavg < long_mavg:
        order_target(context.asset, 0)

    # Save values for later inspection
    record(AAPL=data.current(context.asset, 'price'),
           short_mavg=short_mavg,
           long_mavg=long_mavg)



perf = run_algorithm(start, end, initialize, base_capital, handle_data,
        bundle = 'quantopian-quandl')

perf.to_csv('tearsheet.csv')
plt.figure()
perf.portfolio_value.plot(label="Portfolio value")

plt.legend()
plt.savefig('returns.png')

plt.figure()
perf.AAPL.plot(label='AAPL')
perf.long_mavg.plot(label='Long Moving Average')
perf.short_mavg.plot(label='Short Moving Average')

plt.legend()
plt.savefig('aapl.png')
plt.show()
