import pandas as pd 
import numpy as np 
import statsmodels as sm 
import statistics
import matplotlib.pyplot as plt


param0=0.5
param1=0.3
param2=0.15
param3=0.05

np.set_printoptions(suppress=True, formatter={'float_kind':'{:16.3f}'.format}, linewidth=130)
actualData= pd.read_csv('C:/Users/Ben/iCloudDrive/Workspace/WKUResearch/TrendTrading/ProbModel/Data/SPY.csv')
dailyData = actualData['Price'].values.tolist()
dailyExpecteds= [dailyData[0], dailyData[1], dailyData[2]]


def shortVersion():
    for i in range(3, len(dailyData)):
        #current period
        lagTest0= dailyData[i]	
        #previous period
        lagTest1= dailyData[i-1]
        #two periods ago
        lagTest2= dailyData[i-2]
        #three periods ago
        lagTest3= dailyData[i-3]
        expectedValue= lagTest0*param0+lagTest1*param1+lagTest2*param2+lagTest3*param3
        dailyExpecteds.append(expectedValue)

    sumError= 0
    for i in range(0, len(dailyData)):
        sumError += abs(dailyData[i]-dailyExpecteds[i])

    stdDevs= (1/2)*actualData.rolling(5).std()
    stdDevs['Price'].fillna(0, inplace=True)
    diff= [abs(a_i - b_i) for a_i, b_i in zip(dailyData, dailyExpecteds)]

    print("Correlation between Standard Deviation and Error for Daily", np.corrcoef(stdDevs['Price'], diff)[1, 0])

    plt.plot(stdDevs['Price'], label="Rolling 5-Day Standard Deviation")
    plt.plot(diff, label="Daily Difference")
    plt.legend(loc="best")
    plt.show()

def longVersion():
    actualData= pd.read_csv('C:/Users/Ben/iCloudDrive/Workspace/WKUResearch/TrendTrading/ProbModel/Data/SPY19872017.csv')
    monthlyData = actualData['Price'].values.tolist()
    tempData= np.asarray(monthlyData)
    tempData= np.mean(tempData.reshape(-1, 20), axis=1)
    monthlyData= tempData.tolist()
    monthlyExpecteds= [monthlyData[0], monthlyData[1], monthlyData[2]]

    for i in range(3, len(monthlyData)):
        #current period
        lagTest0= monthlyData[i]	
        #previous period
        lagTest1= monthlyData[i-1]
        #two periods ago
        lagTest2= monthlyData[i-2]
        #three periods ago
        lagTest3= monthlyData[i-3]
        expectedValue= lagTest0*param0+lagTest1*param1+lagTest2*param2+lagTest3*param3
        monthlyExpecteds.append(expectedValue)

    sumError= 0
    for i in range(0, len(monthlyData)):
        sumError += abs(monthlyData[i]-monthlyExpecteds[i])

    monthlyData= pd.DataFrame({'Price':monthlyData})
    stdDevs= (1/2)*monthlyData.rolling(5).std()
    stdDevs['Price'].fillna(0, inplace=True)
    diff= [abs(a_i - b_i) for a_i, b_i in zip(monthlyData['Price'], monthlyExpecteds)]

    print("Correlation between Standard Deviation and Error for Monthly", np.corrcoef(stdDevs['Price'], diff)[1, 0])

    plt.plot(stdDevs['Price'], label="Rolling 5-Month Standard Deviation")
    plt.plot(diff, label="Monthly Difference")
    plt.legend(loc="best")
    plt.show()


if __name__ == "__main__":
    shortVersion()
    longVersion()