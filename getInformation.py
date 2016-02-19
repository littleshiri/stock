# -*- coding:cp949 -*-
# 과거 데이터 다운로드하기

import eBestAPI
import stock
import time

eBestAPI.login('wnsdh10','shiri530','v4vendetta!')

howLong = 350 # 조회기간
items = stock.csvRead(stock.fileRead('items.csv'))

print len(items) , '개의 종목을 조회합니다.'

progress = 0
for item in items:
	progress += 1
	pastData = eBestAPI.getPastData(item[0], howLong)
	stock.fileWrite('C:/Users/Shiri/Desktop/stockData/'+item[0]+item[1]+'.csv',stock.csvWrite(pastData))
	print progress,'/', len(items), item[0], stock.korean(item[1])
	time.sleep(3)