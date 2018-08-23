# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import json
import io
import demjson
app = Flask(__name__)
@app.route('/wehub_api', methods = ['GET','POST'])
def wehub_api():
	if request.method=='POST':
		try:
			request_object = demjson.decode(request.get_data())
		except Exception as e:
			raise e
		finally:
			return  "数据格式错误"
		
		app.logger.debug('recv data:%s',request_object)
		return str(request.get_data())
	elif request.method=='GET':
		app.logger.debug("get:%s",str(request.get_data()))
		return "hello,world"

if __name__ =='__main__':
	app.run(debug = True)