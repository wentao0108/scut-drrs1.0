from django.shortcuts import render
import json
import pymysql
from django.http import HttpResponse
from . import util
from authlib.jose import jwt
import time

def login(request):
	password = request.POST.get('password')
	username = request.POST.get('username')
	if len(password) == 0 or len(username) == 0:
		return util.packApiData(412,'please enter the account password','请输入账号密码',{})
	userid,role,name = userData(username,password)
	
	if userid:
		token = jwt.encode(	{'alg': 'HS256'}, {
			'iss': 'Kudan', 
			'exp': int(time.time()) + 7200 ,
			'userid':userid,
			'name':name,
			'role':role,
			'username':username,
			} 
			,'kexin').decode('UTF-8') 
		return util.packApiData(200,'ok','登录成功',{'token':token})
	else:
		return util.packApiData(403,'default','登录失败',{})