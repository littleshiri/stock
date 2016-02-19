# -*- coding:cp949 -*-

import eBestAPI
import stock
import time
import glob

fileList = glob.glob('C:/Users/Shiri/Desktop/stockData/*.csv')
vectors = []
outcomes = []

for filename in fileList:
	pastData = stock.csvReadNumber(stock.fileRead(filename))
	pos = 0

	while pos < len(pastData)-1 :
		if pastData[pos][3] == pastData[pos][4]:
			pastData.remove(pastData[pos])
		else :
			pos += 1

	# =============== Vector ====================
	if len(pastData) > 100 :
		openp = stock.getVertical(pastData,1)
		closep = stock.getVertical(pastData,2)
		highp = stock.getVertical(pastData,3)
		lowp = stock.getVertical(pastData,4)
		volume = stock.getVertical(pastData,5)
		chdegree = stock.getVertical(pastData,6)
		changerate = stock.getVertical(pastData,7)
		for n in range(4,len(pastData)-30) :
			openDiff1 = (openp[n-1] - closep[n]) / closep[n] * 100
			openDiff2 = (openp[n-2] - closep[n]) / closep[n] * 100
			openDiff3 = (openp[n-3] - closep[n]) / closep[n] * 100
			openDiff4 = (openp[n-4] - closep[n]) / closep[n] * 100
			closeDiff1 = (closep[n-1] - closep[n]) / closep[n] * 100
			closeDiff2 = (closep[n-2] - closep[n]) / closep[n] * 100
			closeDiff3 = (closep[n-3] - closep[n]) / closep[n] * 100
			closeDiff4 = (closep[n-4] - closep[n]) / closep[n] * 100
			ocl = (closep[n-1] - openp[n-1]) / openp[n-1] * 100
			outcomes.append([openDiff1, closeDiff1, openDiff2, closeDiff2, openDiff3, closeDiff3, openDiff4, closeDiff4])

			gap = (openp[n-1] - closep[n]) / closep[n] * 100
			ocl1 = (closep[n] - openp[n]) / openp[n] * 100
			ocl2 = (closep[n+1] - openp[n+1]) / openp[n+1] * 100
			ocl3 = (closep[n+2] - openp[n+2]) / openp[n+2] * 100
			cc1 = (closep[n] - closep[n+1]) / closep[n+1] * 100
			cc2 = (closep[n+1] - closep[n+2]) / closep[n+2] * 100
			cc3 = (closep[n+2] - closep[n+3]) / closep[n+3] * 100
			sum3 = (closep[n] - closep[n+3]) / closep[n+3] * 100
			sum10 = (closep[n] - closep[n+10]) / closep[n+10] * 100
			sum30 = (closep[n] - closep[n+30]) / closep[n+30] * 100
			bar1 = (closep[n] - openp[n]) / (highp[n] - lowp[n])
			bar2 = (closep[n+1] - openp[n+1]) / (highp[n+1] - lowp[n+1])
			bar3 = (closep[n+2] - openp[n+2]) / (highp[n+2] - lowp[n+2])
			pos1 = (closep[n] - lowp[n]) / (highp[n] - lowp[n])
			pos2 = (closep[n+1] - lowp[n+1]) / (highp[n+1] - lowp[n+1])
			pos3 = (closep[n+2] - lowp[n+2]) / (highp[n+2] - lowp[n+2])
			acc1 = cc1-cc2
			acc2 = cc2-cc3
			vectors.append([ocl1, ocl2, ocl3, cc1, cc2, cc3, sum3, sum10, sum30, bar1, bar2, bar3, pos1, pos2, pos3, acc1, acc2, changerate[n]])
			#                0      1    2     3    4    5    6      7      8     9     10    11    12    13    14    15    16         17


# ================== Filtering ======================
tempVector = []
tempY = []
for n in range(0,len(outcomes)) :
	if vectors[n][3]<0 and vectors[n][3]>-14 and vectors[n][15]>0 :
		tempVector.append(vectors[n])
		tempY.append(outcomes[n])
outcomes = tempY
vectors = tempVector
print len(outcomes), len(vectors)

dimension = len(vectors[0])
y = stock.getVertical(outcomes, 3)
for i in range(0,dimension):
	temp = stock.dataNormalize(stock.getVertical(vectors,i))
	for pos in range(0,len(temp)):
		vectors[pos][i] = temp[pos]
normalVector = []
for 
	normalVector.append(0)
for n in range(0,len(y)):
	for i in range(0,dimension):
		normalVector[i] += y[n] * vectors[n][i]
normalVector = stock.vectorNormalize(normalVector)
print stock.vectorNormalize(normalVector)

# ================= Evaluation Part =======================

fit = []
for n in range(0,len(y)):
	fit.append(stock.innerProduct(normalVector,vectors[n]))
b = stock.mean(y)
sumM = 0
count = 0
for n in range(0,len(y)):
	if fit[n] > 0 :
		sumM += (y[n] - b) / fit[n]
		count += 1 
a = sumM / count
for n in range(0,len(fit)):
	#fit[n] = a*fit[n] + b
	print fit[n], y[n]
print stock.corrCoef(fit,y), stock.mean(y)