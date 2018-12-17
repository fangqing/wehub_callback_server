# -*- coding: utf-8 -*-
import logging
from flask import Flask,request
import const
import demjson
import json
import os
import copy
import hashlib

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

g_pull_task_id = 0
#主要的逻辑处理
def main_req_process(wxid,action,request_data_dict):
	app.logger.info("action = {0},data = {1}".format(action,request_data_dict))
	ack_type = 'common_ack'
	if action in const.FIX_REQUEST_TYPES:
		ack_type = str(action)+'_ack'

	if wxid is None or action is None:
		return 1,'参数错误',{},ack_type
	if action=='login':
		nonce = request_data_dict.get("nonce","")
		app.logger.info("nonce = {0}".format(nonce))

		ack_data_dict = {}
		#验证签名
		if len(nonce)>0:
			nonce_str = str(wxid)+'#'+str(nonce)+'#'+str(const.SECRET_KEY)
			md5_object = hashlib.md5()
			md5_object.update(nonce_str.encode("utf-8"))
			app.logger.info("nonce_str = {0},md5 = {1}".format(nonce_str,str(md5_object.hexdigest())))
			ack_data_dict.update({'signature':str(md5_object.hexdigest())})
			
		return 0,"no error",ack_data_dict,ack_type

	if action=='report_friend_add_request':
		reply_data = {
			"v1":request_data_dict.get("v1"),
			"v2":request_data_dict.get("v2"),
			"op_code":1
		}
		return 0,'no error',reply_data,ack_type

	if action=='pull_task':
		#测试代码
		global g_pull_task_id
		g_pull_task_id +=1
		push_msgunit = {
			'msg_type':1,
			'msg':"pull_task,test msg({0}),[微笑]\uE014".format(g_pull_task_id)
		}

		task_data = {
			'task_id':"guid_"+str(g_pull_task_id),
			'task_data':{
				'task_type':1,
				"task_dict":{
					'wxid_to':const.TEST_WXID,
					"msg_list":[push_msgunit]
				}
			}
		}
		return 0,'',task_data,ack_type
	if action=='report_new_msg':		
		msg_unit = request_data_dict.get('msg',{})
		if msg_unit:
			msg_type = msg_unit.get('msg_type',const.MSG_TYPE_INVALID)
			if msg_type in const.UPLOADFILE_MSG_TYPES:
				file_index = msg_unit.get('file_index','')
				if len(file_index)>0 and check_index(file_index):
					task_data = {
						'task_type':const.TASK_TYPE_UPLOAD_FILE,
						'task_dict':{
							'file_index':file_index,
						}
					}
					ack_data_dict = {'reply_task_list':[task_data]}
					return 0,'',ack_data_dict,ack_type
			elif msg_type==4902: #转账
				#这里自动收账
				transferid = msg_unit.get('transferid',"")
				wxid_from = msg_unit.get("wxid_from","")
				wxid_to = msg_unit.get("wxid_to","")
				paysubtype = msg_unit.get("paysubtype",0)
				if paysubtype==1 and wxid_to==wxid:
					task_data ={
						'task_type':11,
						'task_dict':{
							'transferid':transferid,
							'wxid_from':wxid_from
						}
					}
					app.logger.info("begin auto confirm transferid")
					ack_data_dict = {'reply_task_list':[task_data]}
					return 0,'',ack_data_dict,ack_type
			elif msg_type==1:
				msg = msg_unit.get("msg","")
				room_wxid = msg_unit.get("room_wxid","")
				wxid_from = msg_unit.get("wxid_from","")
				app.logger.info("recv chatmsg:{0},from:{1}".format(msg,wxid_from))

				#测试代码
				if wxid_from ==const.TEST_WXID and  msg==str('123'):
					reply_task_list =[]
					if len(room_wxid)>0:
						push_msgunit1 = {
							'msg_type':1,
							'msg':"群消息自动回复,test\ue537"
						}

						push_msgunit2 = {
							'msg_type':3,
							'msg':"https://n.sinaimg.cn/mil/transform/500/w300h200/20180917/OBId-hikxxna1858039.jpg"
						}

						push_msgunit3 = {
							'msg_type':49,
							'link_url':"http://httpd.apache.org/docs/2.4/getting-started.html",
							"link_title":"title",
							"link_desc":"hhhhh_desc",
							"link_img_url":"https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3346649880,432179104&fm=27&gp=0.jpg"
						}

						
						#自动回复群消息
						test_task1 = {
							'task_type':1,
							"task_dict":
							{
								'wxid_to':room_wxid,
								'at_list':[wxid_from],
								"msg_list":[push_msgunit1,push_msgunit2,push_msgunit3]
							}
						}
						reply_task_list.append(test_task1)

					test_task2 = {
						"task_type":1,
						"task_dict":
						{
							"wxid_to":const.TEST_WXID,
							"msg_list":
							[
								{
									'msg_type':1,
									'msg':"wehub文本表情测试,一个商标,一个男人:\ue537\uE138"
								},
								{
									'msg_type':1,
									'msg':"wehub文本表情测试,一个微笑,一个高尔夫:[微笑]\uE014"
								}
							]
						}
					}
					reply_task_list.append(test_task2)
					ack_data_dict = {'reply_task_list':reply_task_list}
					return 0,'',ack_data_dict,ack_type

	return 0,'no error',{},ack_type

def check_index(file_index):
	'''
	检查file_index,自行修改逻辑:对于已经存在的file_index,可以不用重复上传
	'''
	return True

'''
回调接口,处理基本的业务逻辑
request的相关属性见 https://blog.csdn.net/claroja/article/details/80691766
'''
@app.route('/wehub_api', methods = ['POST',"Get"])
def wehub_api():
	if request.method=='POST':
		request_object = request.json #demjson.decode(request.data)
		appid = request_object.get('appid',None)
		action = request_object.get('action',None)
		wxid = request_object.get('wxid',None)
		req_data_dict = request_object.get('data',{})

		if appid is None or action is None or wxid is None:
			rsp_dict = {"error_code":1,"error_reason":'参数错误',"data":{}}
			return  demjson.encode(rsp_dict)

		error_code, error_reason,ack_data,ack_type = main_req_process(wxid,action,req_data_dict)
		ack_dict= {'error_code':error_code,'error_reason':error_reason,'ack_type':str(ack_type),'data':ack_data}
		rsp_data= demjson.encode(ack_dict)
		return rsp_data
	else:
		app.logger.info("recv data is:%s",str(request.get_data()))
		return "<html><body>如果能看到这些内容,说明可以连接到回调接口了,请改用post方式发送</body>"

'''文件上传接口,处理客户端上传的文件,逻辑请自行调整'''
@app.route('/upload_file', methods = ['POST','Get'])
def upload_file():
	if request.method=='POST':
		#取出file_index
		app.logger.info("request.form:{0}".format(request.form))
		file_index = request.form.get('file_index',None)  #从form中提取file_index的值
		app.logger.info("file_index:{0}".format(file_index))
		app.logger.info("request.files:{0}".format(request.files))

		rt_dict = {'error_code':0,'error_reason':'','ack_type':'upload_file_ack','file_index':file_index}

		if 'file' not in request.files:
			app.logger.info("no file part")
			rt_dict.update({'error_code':1,'error_reason':'no file upload'})
			return demjson.encode(rt_dict)

		if not os.path.exists(const.UPLOAD_FOLDER):
			os.makedirs(const.UPLOAD_FOLDER)

		file = request.files['file']
		app.logger.info("file info:{0}".format(file.__dict__))
		file.save(os.path.join(const.UPLOAD_FOLDER,file.filename)) 

		app.logger.info("upload result = {0}".format(rt_dict))
		return demjson.encode(rt_dict)
	else:
		return "<html><body>如果能看到这些内容,说明可以连接到文件上传接口了,请改用post方式发送文件</body>"

if __name__ =='__main__':
	print("server begin")
	#服务器运行在 http://localhost:5678/ 
	#设置回调接口地址为 http://localhost:5678/wehub_api
	#文件上传地址为 http://localhost:5678/upload_file
	app.run(host ='localhost',port =5678,debug = True)
