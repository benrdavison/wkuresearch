import pandas as pd 
import numpy as np 
import statsmodels as sm 
import statistics
import matplotlib.pyplot as plt

show_daily_comparison= False
show_daily_diff= True

show_weekly_comparison= False
show_weekly_diff= False

show_monthly_comparison= False
show_monthly_diff= False

param0=0.5
param1=0.3
param2=0.15
param3=0.05

np.set_printoptions(suppress=True, formatter={'float_kind':'{:16.3f}'.format}, linewidth=130)
actualData= pd.read_csv('C:/Users/Ben/iCloudDrive/Workspace/WKUResearch/TrendTrading/ProbModel/Data/SPY.csv')



def dailyEvaluation(compare, differ):
	
	dailyData = actualData['Price'].values.tolist()
	dailyExpecteds= [dailyData[0], dailyData[1], dailyData[2]]
	
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

	avgError= sumError/len(dailyData)

	print("\n", "DAILY Average Residual between  Predicted Value and Actual Value using Current Lags:", avgError)
	print("\n","Correlation between Actual Data and Predictions", np.corrcoef(dailyData, dailyExpecteds)[1, 0], "\n")


	if compare:
		x = range(len(dailyData))
		y = range(len(dailyData))
		fig = plt.figure()
		ax1 = fig.add_subplot(111)

		plt.plot(dailyData, label="DailyData")
		plt.plot(dailyExpecteds, label="DailyModelResults")
		plt.legend(loc="best")
		plt.show()
	

	if differ:
		x = range(len(dailyData))
		y = range(len(dailyData))
		fig = plt.figure()
		ax1 = fig.add_subplot(111)

		diff= [abs(a_i - b_i) for a_i, b_i in zip(dailyData, dailyExpecteds)]

		plt.plot(diff, label="Daily Difference")
		plt.legend(loc="best")
		plt.show()



def weeklyEvaluation(compare, differ):

	weeklyData = actualData['Price'].values.tolist()
	tempData= np.asarray(weeklyData)
	tempData= np.mean(tempData.reshape(-1, 5), axis=1)
	weeklyData= tempData.tolist()
	weeklyExpecteds= [weeklyData[0], weeklyData[1], weeklyData[2]]

	for i in range(3, len(weeklyData)):
		#current period
		lagTest0= weeklyData[i]	
		#previous period
		lagTest1= weeklyData[i-1]
		#two periods ago
		lagTest2= weeklyData[i-2]
		#three periods ago
		lagTest3= weeklyData[i-3]

		expectedValue= lagTest0*param0+lagTest1*param1+lagTest2*param2+lagTest3*param3
		weeklyExpecteds.append(expectedValue)

	sumError= 0

	for i in range(0, len(weeklyData)):
		sumError += abs(weeklyData[i]-weeklyExpecteds[i])

	avgError= sumError/len(weeklyData)

	print("\n", "WEEKLY Average Residual between Predicted Value and Actual Value using Current Lags:", avgError)
	print("\n","Correlation between Actual Data and Predictions", np.corrcoef(weeklyData, weeklyExpecteds)[1, 0], "\n")


	if compare:
		x = range(len(weeklyData))
		y = range(len(weeklyData))
		fig = plt.figure()
		ax1 = fig.add_subplot(111)

		plt.plot(weeklyData, label="WeeklyData")
		plt.plot(weeklyExpecteds, label="WeeklyModelResults")
		plt.legend(loc="best")
		plt.show()


	if differ:
		x = range(len(weeklyData))
		y = range(len(weeklyData))
		fig = plt.figure()
		ax1 = fig.add_subplot(111)

		diff= [abs(a_i - b_i) for a_i, b_i in zip(weeklyData, weeklyExpecteds)]

		plt.plot(diff, label="Weekly Difference")

		plt.legend(loc="best")
		plt.show()



def monthlyEvaluation(compare, differ):
	
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

	avgError= sumError/len(monthlyData)

	print("\n", "MONTHLY Average Residual between Predicted Value and Actual Value using Current Lags:", avgError)
	print("\n","Correlation between Actual Data and Predictions", np.corrcoef(monthlyData, monthlyExpecteds)[1, 0], "\n")

	
	if compare:
		x = range(len(monthlyData))
		y = range(len(monthlyData))
		fig = plt.figure()
		ax1 = fig.add_subplot(111)

		plt.plot(monthlyData, label="MonthlyData")
		plt.plot(monthlyExpecteds, label="MonthlyModelResults")
		plt.legend(loc="best")
		plt.show()


	if differ:
		x = range(len(monthlyData))
		y = range(len(monthlyData))
		fig = plt.figure()
		ax1 = fig.add_subplot(111)

		diff= [abs(a_i - b_i) for a_i, b_i in zip(monthlyData, monthlyExpecteds)]

		plt.plot(diff, label="Monthly Difference")
		plt.legend(loc="best")
		plt.show()



if __name__ == "__main__":
	
	
	dailyEvaluation(show_daily_comparison, show_daily_diff)
	weeklyEvaluation(show_weekly_comparison, show_weekly_diff)
	monthlyEvaluation(show_monthly_comparison, show_monthly_diff)