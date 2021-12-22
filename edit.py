from django.shortcuts import render
import json
import pymysql
from django.http import HttpResponse
from . import util
from authlib.jose import jwt
import time


def edit(request):
	try:
		claim = jwt.decode(request.headers['Authorization'],'kexin')
		# print(claim)
		username = claim['username']
		role = claim['role']
		if claim['exp'] < int(time.time()):
			return packApiData(40302, 'Token is expired', '令牌已过期，请重新登录')
		creator_id = claim['userid']
		role = claim['role']
	except:
		return util.packApiData(403,'default','请先登录',{})
	if role <= 1:
		return util.packApiData(401,'Insufficient permissions','权限不足',{})
	pid = request.POST.get('pid')
	status = request.POST.get('status')
	connection = pymysql.connect(host ='159.75.47.53',port = 3306,user = "root",passwd = "124536")
	cursor = connection.cursor()
	sql = 'UPDATE data.record SET status = %s WHERE pid = %s'
	cursor.execute(sql,[status,pid])
	connection.commit()
	return util.packApiData(200,'ok','ok',{})