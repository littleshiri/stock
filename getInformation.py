# -*- coding:cp949 -*-
# ���� ������ �ٿ�ε��ϱ�

import eBestAPI
import stock
import time

eBestAPI.login('wnsdh10','shiri530','v4vendetta!')

howLong = 350 # ��ȸ�Ⱓ
items = stock.csvRead(stock.fileRead('items.csv'))

print len(items) , '���� ������ ��ȸ�մϴ�.'

progress = 0
for item in items:
	progress += 1
	pastData = eBestAPI.getPastData(item[0], howLong)
	stock.fileWrite('C:/Users/Shiri/Desktop/stockData/'+item[0]+item[1]+'.csv',stock.csvWrite(pastData))
	print progress,'/', len(items), item[0], stock.korean(item[1])
	time.sleep(3)