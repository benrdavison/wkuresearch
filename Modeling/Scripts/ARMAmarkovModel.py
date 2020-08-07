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

mod_kns = sm.tsa.MarkovRegression(dta_kns, k_regimes=2, trend='nc', switching_variance=True)
res_kns = mod_kns.fit()

print(res_kns.summary())

fig, axes = plt.subplots(2, figsize=(10,7))

ax = axes[0]
ax.plot(res_kns.smoothed_marginal_probabilities[0])
ax.set(title='Smoothed probability of a low-variance regime for stock returns')

ax = axes[1]
ax.plot(res_kns.smoothed_marginal_probabilities[1])
ax.set(title='Smoothed probability of a high-variance regime for stock returns')

fig.tight_layout()
plt.show()


lowVarProbs= res_kns.smoothed_marginal_probabilities[0]
highVarProbs= res_kns.smoothed_marginal_probabilities[1]

raw.columns= ['price']
dataSeries =raw['price']

model = ARIMA(dataSeries, (4,0,0))
model_fit = model.fit(disp=0)

print(model_fit.summary())

predictions = model_fit.predict(start=len(raw), end=len(raw)+5, dynamic=False)
scaledPredictions= (5*predictions)


print("Smoothed Probability of Low Variance in Next Period: {}".format(lowVarProbs[-1]))
print("Smoothed Probability of High Variance in Next Period: {}".format(highVarProbs[-1]))
print("Scaled Prediction of Return in Next Period: {}".format(scaledPredictions[-1]))



