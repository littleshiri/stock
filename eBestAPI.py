# -*- coding:cp949 -*-

import win32com.client
import time
import pythoncom

class LoginEvent:
	queryState = 0
	def OnLogin(self, code, msg):
		self.queryState = 1
		print showTime(), (u"접속이 허가되었습니다. ")		

	def OnLogout(self):
		print("OnLogout method is called")

	def OnDisconnect(self):
		print("OnDisconnect method is called")

class QueryEvent:
	queryState = 0
	def OnReceiveData(self, szTrCode):
		self.queryState = 1
	def OnReceiveMessage(self, bIsSystemError, nMessageCode, szMessage):
		if szMessage != u'조회완료' and szMessage != u'매수 주문이 완료되었습니다.' and szMessage != u'매도 주문이 완료되었습니다.' and szMessage != u'조회가 완료되었습니다.':
			self.queryState = 2
			print szMessage
			print bIsSystemError
			print nMessageCode

class RealEvent:
	queryState = 0
	def OnReceiveRealData(self, szTrCode):
		self.queryState = 1
		print 'asdf'
		print self.GetFieldData('OutBlock','preychange'), self.GetFieldData('OutBlock','shcode'), self.GetFieldData('OutBlock','hotime')
	def OnReceiveLinkData(self, *args):
		print szMessage
		print bIsSystemError
		print nMessageCode

def wait(conn):
	while conn.queryState == 0:
		pythoncom.PumpWaitingMessages()
	if conn.queryState == 2:
		time.sleep(0.5)

def showTime():
	t = time.localtime()
	hours = t.tm_hour
	minuets = t.tm_min
	seconds = t.tm_sec
	return str(hours) + ':' + str(minuets) + ':' + str(seconds)

def login(userId,password,certPass):
 	serverConnector = win32com.client.DispatchWithEvents("XA_Session.XASession", LoginEvent)
 	isServer = serverConnector.ConnectServer('hts.ebestsec.co.kr',20001)
 	if isServer:
 		print showTime(), u'서버 연결됨 '
 	isLogin = serverConnector.Login(userId,password,certPass, 0, True)
 	if isLogin:
 		print showTime(), userId, u'로그인 성공함 '
 	wait(serverConnector)
 	return serverConnector

def eTradeTest(userId,password,certPass):
 	serverConnector = win32com.client.DispatchWithEvents("XA_Session.XASession", LoginEvent)
 	isServer = serverConnector.ConnectServer('127.0.0.1',20001)
 	if isServer:
 		print showTime(), u'서버 연결됨 '
 	isLogin = serverConnector.Login(userId,password,certPass, 0, True)
 	if isLogin:
 		print showTime(), userId, u'로그인 성공함 '
 	wait(serverConnector)
 	return serverConnector

def getAccount(serverConnector):
	account = serverConnector.GetAccountList(0)
	print showTime(), u'계좌 불러오기 완료 '
	return account

def getNowPrice(code):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = "t1102.res"
	serverConnector.SetFieldData('t1102InBlock', 'shcode', 0, code)
	serverConnector.Request(False)
	wait(serverConnector)

	price = float(serverConnector.GetFieldData('t1102OutBlock','price',0))
	diff = float(serverConnector.GetFieldData('t1102OutBlock','diff',0))
	volume = float(serverConnector.GetFieldData('t1102OutBlock','volume',0))
	per = float(serverConnector.GetFieldData('t1102OutBlock','per',0))
	pbrx = float(serverConnector.GetFieldData('t1102OutBlock','pbrx',0))
	high = float(serverConnector.GetFieldData('t1102OutBlock','high',0))
	return [price, diff, volume, high, per, pbrx]

def getWanted(code):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = "t1101.res"
	serverConnector.SetFieldData('t1101InBlock', 'shcode', 0, code)
	serverConnector.Request(False)
	wait(serverConnector)

	offer = float(serverConnector.GetFieldData('t1101OutBlock','offer',0))
	bid = float(serverConnector.GetFieldData('t1101OutBlock','bid',0))
	return offer < bid

def getStockFirm(code):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = "t1102.res"
	serverConnector.SetFieldData('t1102InBlock', 'shcode', 0, code)
	serverConnector.Request(False)
	wait(serverConnector)

	offerno1 = serverConnector.GetFieldData('t1102OutBlock','offerno1',0)
	bidno1 = serverConnector.GetFieldData('t1102OutBlock','bidno1',0)
	return [offerno1, bidno1]

def getMinuetData(code, period):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 't1302.res'
	serverConnector.SetFieldData('t1302InBlock','shcode',0,code)
	serverConnector.SetFieldData('t1302InBlock','gubun',0,period)
	serverConnector.SetFieldData('t1302InBlock','time',0,'')
	serverConnector.SetFieldData('t1302InBlock','cnt',0,'900')
	serverConnector.Request(False)
	wait(serverConnector)

	res = []
	for i in range(0, serverConnector.GetBlockCount('t1302OutBlock1')):
		chetime = int(serverConnector.GetFieldData('t1302OutBlock1','chetime',i))
		close = float(serverConnector.GetFieldData('t1302OutBlock1','close',i))
		diff = float(serverConnector.GetFieldData('t1302OutBlock1','diff',i))
		chdegree = float(serverConnector.GetFieldData('t1302OutBlock1','chdegree',i))
		mdvolumetm = float(serverConnector.GetFieldData('t1302OutBlock1','mdvolumetm',i))
		msvolumetm = float(serverConnector.GetFieldData('t1302OutBlock1','msvolumetm',i))
		totofferrem = float(serverConnector.GetFieldData('t1302OutBlock1','totofferrem',i))
		totbidrem = float(serverConnector.GetFieldData('t1302OutBlock1','totbidrem',i))
		res.append([chetime, close, diff, chdegree, code, mdvolumetm, msvolumetm, totofferrem, totbidrem])
	return res

def getPastData(code, period):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 't1305.res'
	serverConnector.SetFieldData('t1305InBlock','shcode',0,code)
	serverConnector.SetFieldData('t1305InBlock','dwmcode',0,1)
	serverConnector.SetFieldData('t1305InBlock','cnt',0,period)
	serverConnector.Request(False)
	wait(serverConnector)

	res = []
	for i in range(0, serverConnector.GetBlockCount('t1305OutBlock1')):
		date = int(serverConnector.GetFieldData('t1305OutBlock1','date',i))
		close = float(serverConnector.GetFieldData('t1305OutBlock1','close',i))
		popen = float(serverConnector.GetFieldData('t1305OutBlock1','open',i))
		high = float(serverConnector.GetFieldData('t1305OutBlock1','high',i))
		low = float(serverConnector.GetFieldData('t1305OutBlock1','low',i))
		volume = float(serverConnector.GetFieldData('t1305OutBlock1','volume',i))
		chdegree = float(serverConnector.GetFieldData('t1305OutBlock1','chdegree',i))
		sojinrate = float(serverConnector.GetFieldData('t1305OutBlock1','sojinrate',i))
		changerate = float(serverConnector.GetFieldData('t1305OutBlock1','changerate',i))
		res.append([date, popen, close, high, low, volume, chdegree, changerate])
	return res

def getMyMoney():
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 'CSPAQ02200.res'
	serverConnector.SetFieldData('CSPAQ02200InBlock1','RecCnt',0,'1')
	serverConnector.SetFieldData('CSPAQ02200InBlock1','AcntNo',0,'20045705301')
	serverConnector.SetFieldData('CSPAQ02200InBlock1','Pwd',0,'7316')
	serverConnector.Request(False)
	wait(serverConnector)

	return float(serverConnector.GetFieldData('CSPAQ02200OutBlock2','MnyOrdAbleAmt',0))
	

def getHighItems(threshold):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 't1427.res'
	serverConnector.SetFieldData('t1427InBlock','qrygb',0,'2')
	serverConnector.SetFieldData('t1427InBlock','gubun',0,'0')
	serverConnector.SetFieldData('t1427InBlock','signgubun',0,'1')
	serverConnector.SetFieldData('t1427InBlock','diff',0,threshold)
	serverConnector.SetFieldData('t1427InBlock','jc_num',0,0)
	serverConnector.Request(False)
	wait(serverConnector)

	res = []
	for i in range(0, serverConnector.GetBlockCount('t1427OutBlock1')):
		hname = serverConnector.GetFieldData('t1427OutBlock1','hname',i)
		shcode = str(serverConnector.GetFieldData('t1427OutBlock1','shcode',i))
		price = float(serverConnector.GetFieldData('t1427OutBlock1','price',i))
		diff = float(serverConnector.GetFieldData('t1427OutBlock1','diff',i))
		total = float(serverConnector.GetFieldData('t1427OutBlock1','total',i))
		res.append([hname, shcode, price, diff, total])
	return res

def getLowItems(threshold):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 't1427.res'
	serverConnector.SetFieldData('t1427InBlock','qrygb',0,'2')
	serverConnector.SetFieldData('t1427InBlock','gubun',0,'0')
	serverConnector.SetFieldData('t1427InBlock','signgubun',0,'2')
	serverConnector.SetFieldData('t1427InBlock','diff',0,threshold)
	serverConnector.SetFieldData('t1427InBlock','jc_num',0,0)
	serverConnector.Request(False)
	wait(serverConnector)

	res = []
	for i in range(0, serverConnector.GetBlockCount('t1427OutBlock1')):
		hname = serverConnector.GetFieldData('t1427OutBlock1','hname',i)
		shcode = str(serverConnector.GetFieldData('t1427OutBlock1','shcode',i))
		price = float(serverConnector.GetFieldData('t1427OutBlock1','price',i))
		diff = float(serverConnector.GetFieldData('t1427OutBlock1','diff',i))
		total = float(serverConnector.GetFieldData('t1427OutBlock1','total',i))
		res.append([hname, shcode, price, diff, total])
	return res

def getGroupPrice(codelist):
	shcode=''
	for t in codelist:
		shcode += t
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 't8407.res'
	serverConnector.SetFieldData('t8407InBlock','nrec',0,len(codelist))
	serverConnector.SetFieldData('t8407InBlock','shcode',0,shcode)
	serverConnector.Request(False)
	wait(serverConnector)

	res = []
	for i in range(0, serverConnector.GetBlockCount('t8407OutBlock1')):
		hname = serverConnector.GetFieldData('t8407OutBlock1','hname',i)
		price = float(serverConnector.GetFieldData('t8407OutBlock1','price',i))
		diff = float(serverConnector.GetFieldData('t8407OutBlock1','diff',i))
		chdegree = float(serverConnector.GetFieldData('t8407OutBlock1','chdegree',i))
		totofferrem = float(serverConnector.GetFieldData('t8407OutBlock1','totofferrem',i))
		totbidrem = float(serverConnector.GetFieldData('t8407OutBlock1','totbidrem',i))
		value = float(serverConnector.GetFieldData('t8407OutBlock1','value',i))		
		offerho = float(serverConnector.GetFieldData('t8407OutBlock1','offerho',i))
		bidho = float(serverConnector.GetFieldData('t8407OutBlock1','bidho',i))
		res.append([hname, price, diff, chdegree, totofferrem, totbidrem, value, offerho, bidho])
	return res

def getGroupData(codelist):
	shcode=''
	for t in codelist:
		shcode += t
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 't8407.res'
	serverConnector.SetFieldData('t8407InBlock','nrec',0,len(codelist))
	serverConnector.SetFieldData('t8407InBlock','shcode',0,shcode)
	serverConnector.Request(False)
	wait(serverConnector)

	res = []
	for i in range(0, serverConnector.GetBlockCount('t8407OutBlock1')):
		price = float(serverConnector.GetFieldData('t8407OutBlock1','price',i))
		popen = float(serverConnector.GetFieldData('t8407OutBlock1','open',i))
		high = float(serverConnector.GetFieldData('t8407OutBlock1','high',i))
		low = float(serverConnector.GetFieldData('t8407OutBlock1','low',i))
		volume = float(serverConnector.GetFieldData('t8407OutBlock1','volume',i))
		chdegree = float(serverConnector.GetFieldData('t8407OutBlock1','chdegree',i))
		res.append([popen, price, high, low, volume, chdegree])
	return res

def buyStock(code, price, OrdQty):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 'CSPAT00600.res'
	serverConnector.SetFieldData('CSPAT00600InBlock1','AcntNo',0,'20045705301')
	serverConnector.SetFieldData('CSPAT00600InBlock1','InptPwd',0,'7316')
	serverConnector.SetFieldData('CSPAT00600InBlock1','IsuNo',0,code)
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdQty',0,OrdQty)
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdPrc',0,price)
	serverConnector.SetFieldData('CSPAT00600InBlock1','BnsTpCode',0,'2')
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdprcPtnCode',0,'00')
	serverConnector.SetFieldData('CSPAT00600InBlock1','MgntrnCode',0,'000')
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdCndiTpCode',0,'0')
	serverConnector.Request(False)
	wait(serverConnector)

def buyStockNow(code, OrdQty):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 'CSPAT00600.res'
	serverConnector.SetFieldData('CSPAT00600InBlock1','AcntNo',0,'20045705301')
	serverConnector.SetFieldData('CSPAT00600InBlock1','InptPwd',0,'7316')
	serverConnector.SetFieldData('CSPAT00600InBlock1','IsuNo',0,code)
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdQty',0,OrdQty)
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdPrc',0,0)
	serverConnector.SetFieldData('CSPAT00600InBlock1','BnsTpCode',0,'2')
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdprcPtnCode',0,'03')
	serverConnector.SetFieldData('CSPAT00600InBlock1','MgntrnCode',0,'000')
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdCndiTpCode',0,'0')
	serverConnector.Request(False)
	#wait(serverConnector)

def sellStock(code, price, OrdQty):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 'CSPAT00600.res'
	serverConnector.SetFieldData('CSPAT00600InBlock1','AcntNo',0,'20045705301')
	serverConnector.SetFieldData('CSPAT00600InBlock1','InptPwd',0,'7316')
	serverConnector.SetFieldData('CSPAT00600InBlock1','IsuNo',0,code)
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdQty',0,OrdQty)
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdPrc',0,price)
	serverConnector.SetFieldData('CSPAT00600InBlock1','BnsTpCode',0,'1')
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdprcPtnCode',0,'00')
	serverConnector.SetFieldData('CSPAT00600InBlock1','MgntrnCode',0,'000')
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdCndiTpCode',0,'0')
	serverConnector.Request(False)
	wait(serverConnector)

def sellStockNow(code, OrdQty):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 'CSPAT00600.res'
	serverConnector.SetFieldData('CSPAT00600InBlock1','AcntNo',0,'20045705301')
	serverConnector.SetFieldData('CSPAT00600InBlock1','InptPwd',0,'7316')
	serverConnector.SetFieldData('CSPAT00600InBlock1','IsuNo',0,code)
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdQty',0,OrdQty)
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdPrc',0,0)
	serverConnector.SetFieldData('CSPAT00600InBlock1','BnsTpCode',0,'1')
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdprcPtnCode',0,'03')
	serverConnector.SetFieldData('CSPAT00600InBlock1','MgntrnCode',0,'000')
	serverConnector.SetFieldData('CSPAT00600InBlock1','OrdCndiTpCode',0,'0')
	serverConnector.Request(False)
	#wait(serverConnector)

def getHaveItems():
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 'CSPAQ02300.res'
	serverConnector.SetFieldData('CSPAQ02300InBlock1','RecCnt',0,1)
	serverConnector.SetFieldData('CSPAQ02300InBlock1','AcntNo',0,'20045705301')
	serverConnector.SetFieldData('CSPAQ02300InBlock1','Pwd',0,'7316')
	serverConnector.SetFieldData('CSPAQ02300InBlock1','BalCreTp',0,'1')
	serverConnector.SetFieldData('CSPAQ02300InBlock1','CmsnAppTpCode',0,'0')
	serverConnector.SetFieldData('CSPAQ02300InBlock1','D2balBaseQryTp',0,'1')
	serverConnector.SetFieldData('CSPAQ02300InBlock1','UprcTpCode',0,'0')
	serverConnector.Request(False)
	wait(serverConnector)

	res = []
	for i in range(0, serverConnector.GetBlockCount('CSPAQ02300OutBlock3')):
		code = serverConnector.GetFieldData('CSPAQ02300OutBlock3','IsuNo',i)[1:]
		hname = serverConnector.GetFieldData('CSPAQ02300OutBlock3','IsuNm',i)
		SellAbleQty = float(serverConnector.GetFieldData('CSPAQ02300OutBlock3','SellAbleQty',i))
		AvrUprc = float(serverConnector.GetFieldData('CSPAQ02300OutBlock3','AvrUprc',i))
		NowPrc = float(serverConnector.GetFieldData('CSPAQ02300OutBlock3','NowPrc',i))
		PnlRat = float(serverConnector.GetFieldData('CSPAQ02300OutBlock3','PnlRat',i))
		res.append([code, hname, SellAbleQty, AvrUprc, NowPrc, PnlRat])
	return res

def getForeign(code):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = "t1102.res"
	serverConnector.SetFieldData('t1102InBlock', 'shcode', 0, code)
	serverConnector.Request(False)
	wait(serverConnector)

	return (float(serverConnector.GetFieldData('t1102OutBlock','fwsvl',0)) - float(serverConnector.GetFieldData('t1102OutBlock','fwdvl',0))) * float(serverConnector.GetFieldData('t1102OutBlock','price',0)) / 1000000

def getTime():
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = "t0167.res"
	serverConnector.Request(False)
	wait(serverConnector)

	return int(serverConnector.GetFieldData('t0167OutBlock','time',0)[:8])

def getDate():
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = "t0167.res"
	serverConnector.Request(False)
	wait(serverConnector)

	return int(serverConnector.GetFieldData('t0167OutBlock','dt',0))

def getForeignData(code):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = "t1701.res"
	serverConnector.SetFieldData('t1701InBlock', 'shcode', 0, code)
	serverConnector.SetFieldData('t1701InBlock', 'gubun', 0, '0')
	serverConnector.Request(False)
	wait(serverConnector)

	res = []
	for i in range(0, serverConnector.GetBlockCount('t1701OutBlock')):
		date = serverConnector.GetFieldData('t1701OutBlock','date',i)
		price = float(serverConnector.GetFieldData('t1701OutBlock','close',i))
		frgvolume = float(serverConnector.GetFieldData('t1701OutBlock','frgvolume',i))
		res.append([date, price*frgvolume])
	return res

def getBestItems(idx):
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = "t1488.res"
	serverConnector.SetFieldData('t1488InBlock', 'gubun', 0, '0')
	serverConnector.SetFieldData('t1488InBlock', 'sign', 0, '2')
	serverConnector.SetFieldData('t1488InBlock', 'jgubun', 0, '1')
	serverConnector.SetFieldData('t1488InBlock', 'idx', 0, idx)
	serverConnector.Request(True)
	wait(serverConnector)
	res = []
	for i in range(0, serverConnector.GetBlockCount('t1488OutBlock1')):
		hname = serverConnector.GetFieldData('t1488OutBlock1','hname',i)
		shcode = serverConnector.GetFieldData('t1488OutBlock1','shcode',i)
		price = float(serverConnector.GetFieldData('t1488OutBlock1','price',i))
		diff = float(serverConnector.GetFieldData('t1488OutBlock1','diff',i))
		res.append([hname, shcode, price, diff])
	return res

def getProfit():
	serverConnector = win32com.client.DispatchWithEvents('XA_DataSet.XAQuery', QueryEvent)
	serverConnector.ResFileName = 'CSPAQ02300.res'
	serverConnector.SetFieldData('CSPAQ02300InBlock1','RecCnt',0,'1')
	serverConnector.SetFieldData('CSPAQ02300InBlock1','AcntNo',0,'20045705301')
	serverConnector.SetFieldData('CSPAQ02300InBlock1','Pwd',0,'7316')
	serverConnector.SetFieldData('CSPAQ02300InBlock1','CmsnAppTpCode',0,'1')
	serverConnector.Request(False)
	wait(serverConnector)

	return float(serverConnector.GetFieldData('CSPAQ02300OutBlock2','EvalPnlSum',0))

# Real 이벤트에서 문제 생겨서 임시 블럭
# KOSPIconnector = win32com.client.DispatchWithEvents('XA_DataSet.XAReal', RealEvent)
# KOSDAQconnector = win32com.client.DispatchWithEvents('XA_DataSet.XAReal', RealEvent)

def setItems(items):
	KOSPIconnector.items = items
	KOSPIconnector.LoadFromResFile('YS3.res')
	KOSDAQconnector.items = items
	KOSDAQconnector.LoadFromResFile('YK3.res')

def adviseKOSPI(nth):
	KOSPIconnector.SetFieldData( 'InBlock', 'shcode', KOSPIconnector.items[nth][0] )
	KOSPIconnector.AdviseRealData()