# -*- coding: utf-8 -*-
from  http.client  import HTTPConnection 
import json
import demjson
import const
send_dict = {'action':'login','appid':'12345','wxid':'fangqing_hust','data':{'mydata':'xxxxx'}}
header_data = {"Content-type":"application/json","Accept": "text/plain"}
conn = HTTPConnection(const.BIND_HOST,const.BIND_PORT)
r = conn.request('post','/wehub_api',body = demjson.encode(send_dict),headers = header_data)
respone = conn.getresponse()
data = respone.read()
print(data)