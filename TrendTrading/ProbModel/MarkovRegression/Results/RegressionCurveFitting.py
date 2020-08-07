import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

actualData= pd.read_csv('C:/Users/Ben/iCloudDrive/Workspace/XiaResearch/TrendTrading/ProbModel/Data/SPY.csv')
actualData = actualData['Price'].values.tolist()
indices= []

for i in range(1, len(actualData)+1):
	indices.append(i)

indices= np.array(indices)
actualData= np.array(actualData)

firstFit= np.polyfit(indices, actualData, 1)
secondFit= np.polyfit(indices, actualData, 2)
thirdFit= np.polyfit(indices, actualData, 3)
fourthFit= np.polyfit(indices, actualData, 4)

firstFunc= np.poly1d(firstFit)
secondFunc= np.poly1d(secondFit)
thirdFunc= np.poly1d(thirdFit)
fourthFunc= np.poly1d(fourthFit)

print(firstFunc, "\n")
print(secondFunc, "\n")
print(thirdFunc, "\n")
print(fourthFunc)


plt.plot(indices, firstFunc(indices))
plt.plot(indices, secondFunc(indices))
plt.plot(indices, thirdFunc(indices), '--')
plt.plot(indices, fourthFunc(indices))
plt.plot(indices, actualData)

plt.legend(loc="best")
plt.show()