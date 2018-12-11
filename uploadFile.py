# -*- coding: utf-8 -*-
import requests
import demjson
import const
'''
 模拟wehub上传一条图片消息(附带该图片的file_index),服务返回告诉wehub是否需要上传消息中的图片
 这个逻辑纯粹是为了节省流量.
'''
def uploadFile(file_index):
	'''模拟wehub上传文件'''
	url = 'http://127.0.0.1:5678/upload_file'   #文件上传接口地址

	#测试代码:换成你要测试上传的文件
	file_data={'file':open('d:/test.jpg','rb')}    
	post_data = {'file_index':file_index}     

	#fiddler的默认代理是 127.0.0.1:8888,这种方式可以方便的在fiddler中查看http的request

	#proxies 参数可以留空
	rsp = requests.post(url,files = file_data,data = post_data,proxies ={'http':'127.0.0.1:8888'})  
	rt_dict= demjson.decode(rsp.text)
	print (rt_dict)  


def report_image_msg():
	'''模式wehub上报一条图片消息'''
	msg_unit = {
		'msg_type':const.MSG_TYPE_IMAGE,
		'room_wxid':'xxxx@chatroom',
		'wxid':'xxxxx',
		#file_index 的值是微信中原生的文件索引值,wehub不做特殊处理
		'file_index':'3053020100044c304a02010002041cdc709b02032f56c10204e3e5e77302045b84b6b10425617570696d675f356665376666383735333737623337355f313533353432343137353938360204010400020201000400'
	}

	header_data = {"Content-type":"application/json"}
	send_dict = {'action':'report_new_msg','appid':'12345','wxid':'fangqing_hust','data':{'msg':msg_unit.copy()}}
	url = 'http://127.0.0.1:5678/wehub_api'   #回调接口地址
	rsp = requests.post(url,data = demjson.encode(send_dict),headers = header_data)

	rt_dict = demjson.decode(rsp.text)

	#回调接口返回是否需要上传文件的respone
	print ('rt_dict',rt_dict)
	if rt_dict['ack_type']=='report_new_msg_ack':
		reply_task_list = rt_dict['data'].get('reply_task_list',[])
		for task_item in reply_task_list:
			print ('task_item',task_item)
			if task_item['task_type']==const.TASK_TYPE_UPLOAD_FILE:
				data_dict = task_item['task_dict']
				file_index = data_dict.get('file_index',None)
				print ("file_index = ",file_index)
				flag = data_dict.get('flag',1)
				if flag==1:
					uploadFile(file_index)
				else:
					pass

if __name__ =='__main__':
	report_image_msg()