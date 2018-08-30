# -*- coding: utf-8 -*-
import requests
import demjson
import const
'''
 模拟wehub上传一条图片消息(附带该图片的file_index),服务返回告诉wehub是否需要上传消息中的图片
 这个逻辑纯粹是为了节省流量.
'''
def get_file_path_by_index(file_index):
	return 'd:/20180828104732.jpg';            #这只是我测试的一个文件,请替换

def uploadFile(file_index):
	'''模拟wehub上传文件'''
	url = 'http://127.0.0.1:5678/upload_file'   #这里替换成第三方自定义的文件上传接口地址

	file_data={'file':open(get_file_path_by_index(file_index),'rb')}  
	post_data = {'file_index':file_index}     

	#fiddler的默认代理是 127.0.0.1:8888,这种方式可以方便的在fiddler中查看http的request
	#rsp = requests.post(url,files = file_data,data = post_data,proxies ={'http':'127.0.0.1:8888'})  
	rsp = requests.post(url,files = file_data,data = post_data)
	rt_dict= demjson.decode(rsp.text)
	print (rt_dict)  



def report_image_msg():
	'''模式wehub上报一条图片消息,回调接口返回是否需要上传文件的respone'''
	msg_unit = {
		'msg_type':const.MSG_TYPE_IMAGE,
		'room_wxid':'xxxx@chatroom',
		'wxid':'xxxxx',
		#file_index 的值是微信中原生的文件索引值,wehub不做特殊处理
		'file_index':'3053020100044c304a02010002041cdc709b02032f56c10204e3e5e77302045b84b6b10425617570696d675f356665376666383735333737623337355f313533353432343137353938360204010400020201000400'
	}

	header_data = {"Content-type":"application/json"}
	send_dict = {'action':'report_new_msg','appid':'12345','wxid':'fangqing_hust','data':{'msg':msg_unit.copy()}}
	url = 'http://127.0.0.1:5678/wehub_api'
	rsp = requests.post(url,data = demjson.encode(send_dict),headers = header_data)

	rt_dict = demjson.decode(rsp.text)

	print ('rt_dict',rt_dict)
	if rt_dict['ack_type']=='report_new_msg_ack':
		reply_task_list = rt_dict['data'].get('reply_task_list',[])
		for task_item in reply_task_list:
			if task_item['task_type']==const.TASK_TYPE_UPLOAD_FILE:
				file_index = task_item.get('file_index')
				op_code = task_item.get('op_code')
				if op_code==1:
					uploadFile(file_index)
				else:
					print ('不用重复上传')

if __name__ =='__main__':
	report_image_msg()