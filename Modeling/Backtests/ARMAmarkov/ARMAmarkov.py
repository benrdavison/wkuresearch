'''
Created on Mar 26, 2019

@author: ben
'''
from zipline.api import order_target_percent, record, symbol, set_benchmark #@UnresolvedImport
from zipline import run_algorithm
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA

base_capital = 100000
start = datetime(2009, 1, 1, 0, 0, 0, 0, pytz.utc)
end = datetime(2010, 1, 1, 0, 0, 0, 0, pytz.utc)


def initialize(context):
    context.i = 0
    set_benchmark(symbol('AAPL'))
    context.asset = symbol('AAPL')


def handle_data(context, data):
    context.i +=1
    print(context.i)
    position= context.portfolio.positions[context.asset].amount
    
    raw= data.history(context.asset, 'price', bar_count=100, frequency="1d")
    raw= raw.dropna()

    
    returns = raw.pct_change()
    returns= returns.iloc[1:]
    

    
    dta_kns = returns- returns.mean()

    mod_kns = sm.tsa.MarkovRegression(dta_kns, k_regimes=2, trend='nc', switching_variance=True)
    res_kns = mod_kns.fit()

    
    lowVarProbs= res_kns.smoothed_marginal_probabilities[0]
    highVarProbs= res_kns.smoothed_marginal_probabilities[1]
    
    model = ARIMA(returns, (4,0,0))
    model_fit = model.fit(disp=0)
    
    predictions = model_fit.predict(start=len(returns), end=len(returns)+5, dynamic=False)
    scaledPredictions= (predictions)
    

    
    if(lowVarProbs[-1] >= highVarProbs[-1]):
        if(scaledPredictions[-1] > 0): 
            if (position ==0):
                order_target_percent(context.asset, lowVarProbs[-1])
                
            else:
                pass
        else:
            order_target_percent(context.asset, 0)
        
    else:
        pass

    record(AAPL=data.current(context.asset, 'price'),
           lowVarProb=lowVarProbs[-1],
           highVarProb=highVarProbs[-1])


perf = run_algorithm(start, end, initialize, base_capital, handle_data,
        bundle = 'quantopian-quandl')
perf.to_csv('tearsheet.csv')

plt.figure()
perf.portfolio_value.plot(label="Portfolio value")
plt.legend()
plt.savefig('returns.png')

plt.figure()
perf.AAPL.plot(label='AAPL')
plt.legend()
plt.savefig('aapl.png')

plt.figure()
perf.lowVarProb.plot(label='Probability of Low Variance')
perf.highVarProb.plot(label='Probability of High Variance')
plt.legend()
plt.savefig('varprobs.png')

plt.show()


