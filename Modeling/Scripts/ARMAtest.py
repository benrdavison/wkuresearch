'''
Created on Mar 25, 2019

@author: ben
'''
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt 

from statsmodels.tsa.arima_model import ARIMA

# Get the dataset
raw = pd.read_csv("C:/Users/New User/iCloudDrive/Workspace/WKUResearch/Modeling/Data/SPYreturns.csv", header=None)
raw.index = pd.date_range('2017-01-01', periods=len(raw), freq='D')


dta_kns = raw- raw.mean()


raw.columns= ['price']
dataSeries =raw['price']


model = ARIMA(dataSeries, (4,0,0))

model_fit = model.fit(disp=0)

print('Coefficients: %s' % model_fit.params)
predictions = model_fit.predict(start=len(raw), end=len(raw)+5, dynamic=False)
print(predictions[-1])

plt.plot(dataSeries)
plt.legend(loc="best")
plt.plot(4*predictions)
plt.legend(loc="best")

plt.show()



