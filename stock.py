# -*- coding: cp949 -*-
import glob
from math import *
import urllib

def korean(text):
	return text.decode('cp949').encode('cp949')
def summ(data):
	res = 0
	for i in data:
		res += i
	return res
def mean(data):
	if len(data)==0:
		return 0
	else : 
		return sum(data)/float(len(data))
def variance(data):
	square = 0
	for n in data:
		square += n**2
	square /= float(len(data))
	return square - mean(data)**2
def std(data):
	return sqrt(variance(data))
def bias(data, origin):
	dist = 0
	for i in data : 
		dist += (i-origin)*(i-origin)
	return sqrt(dist/len(data))
def rateDiffer(data):
	res = []
	for i in range(0,len(data)-1):
		res.append((data[i]/(data[i+1]+0.000001)-1)*100)
	return res
def movMean(data, days):
	res = []
	for i in range(0,len(data)-days+1):
		s = 0
		count = 0
		for n in range(0,days):
			count += days-n
			s += data[i+n]*(days-n)
		res.append(s/count)
	return res
def corrCoef(X,Y):
	sumXY = 0
	meanX = mean(X)
	meanY = mean(Y)
	stdX = std(X)
	stdY = std(Y)
	for i in range(0,len(X)):
		sumXY += X[i] * Y[i]
	sumXY /= float(len(X))
	return (sumXY - meanX*meanY) / (stdX*stdY)
def vectorNormalize(vector):
	square = 0
	for element in vector:
		square += element**2
	res = []
	for element in vector:
		res.append(element/sqrt(square))
	return res
def dataNormalize(data):
	stdData = std(data)
	meanData = mean(data)
	res = []
	for d in data:
		res.append((d-meanData)/stdData)
	return res
def innerProduct(vector1,vector2):
	res = 0
	for i in range(0,len(vector1)):
		res += vector1[i]*vector2[i]
	return res
def normalDist(x,h):
	return exp(-0.5*(x/h)*(x/h))
def getVertical(data,num):
	res = []
	for i in data:
		res.append(i[num])
	return res
def csvWrite(data):
	text = ''
	for line in data:
		for num in line :
			text += str(num)+','
		text = text[:-1]+'\n'
	return text[:-1]
def fileRead(filename):
	f = open(filename,'r')
	text = f.read()
	f.close()
	return text
def fileWrite(filename,data):
	f = open(filename,'w')
	f.write(data)
	f.close()
def csvReadNumber(text):
	res = []
	lines = text.split('\n')
	for line in lines :
		numbers = line.split(',')
		temp = []
		for number in numbers:
			try :
				temp.append(float(number))
			except ValueError:
				temp.append(number)
		res.append(temp)
	return res
def csvRead(text):
	res = []
	lines = text.split('\n')
	for line in lines :
		numbers = line.split(',')
		res.append(numbers)
	return res
def getLast(data):
	#
	return data[-1]
def getFirst(data):
	return data[0]

def importData (filename) :
	f = open(filename, 'r')
	text = f.read()
	f.close()
	lines = text.split('\n')
	data = []
	for line in lines :
		numbers = line.split(',')
		numberData = []
		for number in numbers : 
			numberData.append(float(number))
		data.append(numberData)
	return data

def getInformation (data, days):
	lines = []
	pOpen, pClose, pHigh, pLow, pTrade, pCircle = [], [], [], [], [], []
	for day in range(0,len(data)) :
		pOpen.append(data[day][1])
		pClose.append(data[day][2])
		pHigh.append(data[day][3])
		pLow.append(data[day][4])
		pTrade.append(data[day][5])
		pCircle.append(data[day][7])
	rClose = rateDiffer(pClose)
	srClose = rateDiffer(movMean(pClose,3))
	trend = rateDiffer(movMean(pClose,5))
	s = std(rClose)
	for day in days :
		obj = [0,0,0,0,0,0,0,0,0]
		if day>0:
			obj[0] = (pClose[day-1]/(pOpen[day-1]+1)-1)*100
			if obj[0]<-14:
				obj[0] = -14
		else :
			obj[0] = 0
		obj[1] = pOpen[day-1]/pClose[day]
		obj[2] = rClose[day+0]
		obj[3] = mean(pTrade[day:day+50])*pClose[day]>300000000
		obj[4] = rClose[day+1]
		obj[5] = True
		obj[6] = rClose[day+2]
		lines.append(obj)

	return lines

def getNormalData(data, threshold):
	res = []
	for i in data:
		if i[0] <= threshold:
			res.append(i)
	return res
def getGoodData(data, threshold):
	res = []
	for i in data:
		if i[0] > threshold:
			res.append(i)
	return res

def computeParzen(normalData, goodData):
	ratio = float(len(goodData))/float(len(goodData)+len(normalData))
	scoreMap = []
	for t in range(1,7):
		s = std(getVertical(goodData+normalData,t))
		minimap = []

		for i in range(0,300) :
			pGood = 0
			pNormal = 0
			x = float(i)/10-15
			for d in goodData:
				pGood += normalDist(d[t]-x,s*0.5)
			for d in normalData:
				pNormal += normalDist(d[t]-x,s*0.5)
			minimap.append((pGood/(pGood+pNormal+0.001)-ratio)*100)
			print i, pGood/(pGood+pNormal+0.001)*100

		print t
		scoreMap.append(minimap)

	return scoreMap

def evaluate(day):
	res = 0
	if day[3] and -14<day[2]<0.5 and day[4]<0.5:
		res += 2 - day[1] 
	return res

def getGoogleStock(market,code):
	text = urllib.urlopen('http://www.google.com/finance?q='+market+'%3A'+code).read()
	pos = text.find('<meta itemprop="priceChangePercent"')
	text = text[pos:pos+1000]
	pos = text.find('content')
	text = text[pos+9:]
	pos = text.find('"')
	text = text[:pos]
	try :
		return float(text)
	except ValueError:
		return 0