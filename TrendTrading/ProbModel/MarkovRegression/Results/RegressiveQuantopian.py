import pandas as pd 
import numpy as np 
import talib



np.set_printoptions(suppress=True, formatter={'float_kind':'{:16.3f}'.format}, linewidth=130)
param0=0.5
param1=0.3
param2=0.15
param3=0.05

def initialize(context):
    
    context.spy= sid(8554)    
    schedule_function(func=trade, date_rule=date_rules.every_day())
    
    
def trade(context, data):
    
    position = context.portfolio.positions[context.spy].amount
    
    prices= data.history(context.spy, 'price', 5, '1d')
    
    lagTest0= prices[len(prices)-1]
    lagTest1= prices[len(prices)-2]
    lagTest2= prices[len(prices)-3]
    lagTest3= prices[len(prices)-4]
    

    expectedValue= lagTest0*param0+lagTest1*param1+lagTest2*param2+lagTest3*param3

    if expectedValue > lagTest0 and position == 0:
        order_target_percent(context.spy, 1)
        
    elif expectedValue < lagTest0 and position > 0:
        order_target_percent(context.spy, 0)
        
    record(lev=context.account.leverage)