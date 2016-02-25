<<<<<<< HEAD
# -*- coding:cp949 -*-

import eBestAPI
import stock
import time

eBestAPI.login('wnsdh10','shiri530','v4vendetta!')
items = stock.csvRead(stock.fileRead('items.csv'))
today = eBestAPI.getDate()

print '오늘은',today,'입니다.'

while len(items) > 0:
	codelist = items[:50]
	items = items[50:]
	groupData = eBestAPI.getGroupData(stock.getVertical(codelist,0))
	pos = 0
	for data in groupData :
		temp = [today] + data
		pastDataList = stock.csvRead(stock.fileRead('C:/Users/Shiri/Desktop/stockData/'+codelist[pos][0]+codelist[pos][1]+'.csv'))
		pastData = pastDataList[0]
		if len(pastData) == 1 or len(temp) == 1:
			continue
		if temp[1]==float(pastData[1]) and temp[2]==float(pastData[2]) and temp[3]==float(pastData[3]) and temp[4]==float(pastData[4]) : 
			pass
		else :
			if float(pastData[5]) == 0 :
				temp += [0]
			else :
				temp += [int(float(pastData[7])*temp[5]/float(pastData[5])*100)/100.0]
			pastDataList = [[temp]] + pastDataList
			stock.fileWrite('C:/Users/Shiri/Desktop/stockData/'+codelist[pos][0]+codelist[pos][1]+'.csv', pastDataList)
			pass
		pos += 1
=======
# -*- coding:cp949 -*-

import eBestAPI
import stock
import time

eBestAPI.login('wnsdh10','shiri530','v4vendetta!')
items = stock.csvRead(stock.fileRead('items.csv'))
today = eBestAPI.getDate()

print '오늘은',today,'입니다.'

while len(items) > 0:
	codelist = items[:50]
	items = items[50:]
	groupData = eBestAPI.getGroupData(stock.getVertical(codelist,0))
	pos = 0
	for data in groupData :
		temp = [today] + data
		pastDataList = stock.csvRead(stock.fileRead('C:/Users/Shiri/Desktop/stockData/'+codelist[pos][0]+codelist[pos][1]+'.csv'))
		pastData = pastDataList[0]
		if len(pastData) == 1 or len(temp) == 1:
			continue
		if temp[1]==float(pastData[1]) and temp[2]==float(pastData[2]) and temp[3]==float(pastData[3]) and temp[4]==float(pastData[4]) : 
			pass
		else :
			if float(pastData[5]) == 0 :
				temp += [0]
			else :
				temp += [int(float(pastData[7])*temp[5]/float(pastData[5])*100)/100.0]
			pastDataList = [[temp]] + pastDataList
			stock.fileWrite('C:/Users/Shiri/Desktop/stockData/'+codelist[pos][0]+codelist[pos][1]+'.csv', pastDataList)
			pass
		pos += 1
>>>>>>> 022958380d77c669255e959a6e47624fa199a980
	time.sleep(0.2)