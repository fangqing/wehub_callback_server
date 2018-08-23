# -*- coding: utf-8 -*-
import logging
from flask import Flask
from flask import request
import const
import demjson
app = Flask(__name__)
app.config.update(debug=True)
app.logger.setLevel(logging.INFO)
@app.route('/wehub_api', methods = ['GET','POST'])
def wehub_api():
	if request.method=='POST':
		try:
			app.logger.info('recv data:%s',request.get_data())
			request_object = demjson.decode(request.get_data())
		except Exception as e:
			app.logger.error("parse json data error")
			return  demjson.encode("数据格式错误")
		finally:
			pass
		return request.get_data()
	elif request.method=='GET':
		app.logger.debug("get:%s",str(request.get_data()))
		return "hello,world"

if __name__ =='__main__':
	app.run(host = const.BIND_HOST,port = const.BIND_PORT,debug = True)
