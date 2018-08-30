# -*- coding: utf-8 -*-
import logging
from flask import Flask,request
import const
import demjson
import json
import os
import copy
UPLOAD_FOLDER = 'd:/test_uploads'   #换成服务端的文件存储路径

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.logger.setLevel(logging.INFO)

#主要的逻辑处理
def main_req_process(wxid,action,request_data_dict):
	if wxid is None or action is None:
		return 1,'参数错误',{}

	app.logger.info("request_data_dict:{0}".format(request_data_dict))

	if action=='report_new_msg':		#上报聊天消息
		msg_unit = request_data_dict.get('msg',{})
		if msg_unit:
			msg_type = msg_unit.get('msg_type',const.MSG_TYPE_INVALID)
			if msg_type in const.UPLOADFILE_MSG_TYPES:
				file_index = msg_unit.get('file_index','')
				
				flag = 1
				if is_file_index_exist(file_index):
					flag = 0

				task_data ={
					'task_type':const.TASK_TYPE_UPLOAD_FILE,
					'task_dict':{
						'file_index':file_index,
						'flag':flag
					}
				}
				ack_data_dict = {'reply_task_list':[task_data]}
				return 0,'',ack_data_dict

	return 0,'no error',{}

def is_file_index_exist(file_index):
	'''检查file_index所代表的文件是否已经存在'''
	return False

'''
回调接口,处理基本的业务逻辑
request的相关属性见 https://blog.csdn.net/claroja/article/details/80691766
'''
@app.route('/wehub_api', methods = ['POST'])
def wehub_api():
	if request.method=='POST':
		request_object = request.json #demjson.decode(request.data)
		app.logger.info("request json = %s",request_object)
		
		appid = request_object.get('appid',None)
		action = request_object.get('action',None)
		wxid = request_object.get('wxid',None)
		req_data_dict = request_object.get('data',{})

		if appid is None or action is None or wxid is None:
			rsp_dict = {"error_code":1,"error_reason":'参数错误',"data":{}}
			return  demjson.encode(rsp_dict)

		error_code, error_reason,ack_data = main_req_process(wxid,action,req_data_dict)
		app.logger.info("ack_data:{0}".format(ack_data))
		ack_dict= {'error_code':error_code,'error_reason':error_reason,'ack_type':str(action)+'_ack','data':ack_data}
		rsp_data= demjson.encode(ack_dict)
		app.logger.info("send respone:{0}".format(rsp_data))
		return rsp_data
	else:
		app.logger.info("recv data is:%s",str(request.get_data()))
		return "暂时只支持Post方式"

'''文件上传接口,处理客户端上传的文件'''
@app.route('/upload_file', methods = ['POST'])
def upload_file():
	if request.method=='POST':
		#取出file_index
		app.logger.info("request.form:{0}".format(request.form))
		file_index = request.form['file_index']   #从form中提取file_index的值
		app.logger.info("file_index:{0}".format(file_index))
		app.logger.info("request.files:{0}".format(request.files))

		rt_dict = {'error_code':0,'error_reason':'','ack_type':'upload_file_ack','file_index':file_index}

		if 'file' not in request.files:
			app.logger.info("no file part")
			rt_dict.update({'error_code':1,'error_reason':'no file upload'})
			return demjson.encode(rt_dict)

		if not os.path.exists(UPLOAD_FOLDER):
			os.makedirs(UPLOAD_FOLDER)

		file = request.files['file']
		app.logger.info("file info:{0}".format(file.__dict__))
		file.save(os.path.join(UPLOAD_FOLDER,file.filename)) 

		app.logger.info("upload result = {0}".format(rt_dict))
		return demjson.encode(rt_dict)


if __name__ =='__main__':
	app.run(host ='localhost',port =5678,debug = True)
