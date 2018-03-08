# -*- coding: utf-8 -*-
import requests
import time
import json
import base64
import chardet

appkey = "7cd47959b2d14beeac9f1a0c87350d66"
memobirdID = "75893a960d133bd5"
useridentifying = "icentasy"
timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
userBindURL = "http://open.memobird.cn/home/setuserbind?ak=%s&timestamp=%s&memobirdID=%s&useridentifying=%s" % (appkey, timestamp, memobirdID, useridentifying)
printPaperURL = "http://open.memobird.cn/home/printpaper"
userID = None

def requestURL(url, data=None):
	j = None
	try:
		res = None
		if data is None:
			res = requests.get(url)
		else:
			header = {"Content-Type": "application/json; charset=utf-8"}
			res = requests.post(url, data=data, headers=header)
		if res.status_code == 200:
			j = json.loads(res.content)
		else:
			print "request error! Msg:%s code:%d" % (res.reason, res.status_code)
	except Exception, e:
		print e
	finally:
		return j

def bindUser():
	global userID
	j = requestURL(userBindURL)
	print json.dumps(j)
	if j["showapi_res_code"] == 1:
		userID = j["showapi_userid"]
		return True
	return False

def printContent(content):
	data = {
		"ak": appkey,
		"timestamp": timestamp,
		"printcontent": "T:"+base64.b64encode(content),
		"memobirdID": memobirdID,
		"userID": userID}
	print json.dumps(data)
	j = requestURL(printPaperURL, json.dumps(data))
	print json.dumps(j)
	if j["showapi_res_code"] == 1:
		return True
	return False

if __name__ == '__main__':
	# print chardet.detect("我的一张小纸条")
	if bindUser():
		printContent("我的一张小纸条".decode("utf-8").encode("gbk"))
