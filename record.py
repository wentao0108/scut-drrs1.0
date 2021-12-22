from django.shortcuts import render
import json
import pymysql
from django.http import HttpResponse
from . import util
from authlib.jose import jwt
import time


def record(request):
	try:
		claim = jwt.decode(request.headers['Authorization'],'kexin')
		# print(claim)
		username = claim['username']
		role = claim['role']
		if claim['exp'] < int(time.time()):
			return packApiData(40302, 'Token is expired', '令牌已过期，请重新登录')
		creator_id = claim['userid']
		role = claim['role']
		print(creator_id)
	except:
		return util.packApiData(403,'default','请先登录',{})
	connection = pymysql.connect(host ='159.75.47.53',port = 3306,user = "root",passwd = "124536")
	cursor = connection.cursor()
	if role <= 1:
		sql = 'SELECT name,address,content,time_stamp,repairman,status,phone,pid FROM data.record WHERE creator_id = %s ORDER BY id DESC'
	# sql = 'desc data.record'
		cursor.execute(sql,[creator_id])
	else:
		sql = 'SELECT name,address,content,time_stamp,repairman,status,phone,pid FROM data.record ORDER BY id DESC'
		cursor.execute(sql)
	result = cursor.fetchall()
	event_list = []
	try:
		for record in result:
			name,address,content,time_stamp,repairman,status,phone,pid = record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7]
			appoint = time_stamp
			event_list.append({'name':name,'address':address,'phone':phone,'content':content,'appoint':appoint,'repairman':repairman,'status':status,'pid':pid})
	except:
		return util.packApiData(401,'lack of data','缺少数据',{})
	return util.packApiData(200,'ok','成功',{'role':role,'username':username,'creator_id':creator_id,'record':event_list})
	# 报修记录