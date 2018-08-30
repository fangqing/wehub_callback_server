# -*- coding: utf-8 -*-
from  http.client  import HTTPConnection 
import json
import demjson
import const
import io

#模拟wehub 向回调接口post  json数据
def client_post():
	send_dict = {'action':'xxxxxxx','appid':'12345','wxid':'方清','data':{'xxx':'xxx任何可能的测试数据'}}
	header_data = {"Content-type":"application/json"}
	conn = HTTPConnection('localhost',5678)

	send_buf_data = demjson.encode(send_dict)
	r = conn.request('post','/wehub_api',body = send_buf_data,headers = header_data)
	respone_bytes = conn.getresponse().read()
	print("respone = {0}".format(demjson.decode(respone_bytes)))

if __name__ =='__main__':
	client_post()


