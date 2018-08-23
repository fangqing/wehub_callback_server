# -*- coding: utf-8 -*-
from  http.client  import HTTPConnection 
import json
import demjson
send_dict = {'action':'login','appid':'12345','wxid':'fangqing_hust','data':{'mydata':'xxxxx'}}
header_data = {"Content-type":"application/json","Accept": "text/plain"}
conn = HTTPConnection("127.0.0.1:5000")
r = conn.request('post','/wehub_api',body = demjson.encode(send_dict),headers = header_data)
respone = conn.getresponse()

data = respone.read()
print(data)