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
	url = 'http://192.168.1.200:5678/upload_file'   #文件上传接口地址
	#测试代码:换成你要测试上传的文件
	#实际上wehub会根据file_index去找到对应的文件,进行上传,这里是直接写固定的文件做测试
	file_data={'file':open('d:/test.pic','rb')}    
	post_data = {'file_index':file_index}     

	#fiddler的默认代理是 127.0.0.1:8888,这种方式可以方便的在fiddler中查看http的request
	#如果你没有开fiddler,proxies参数请留空
	rsp = requests.post(url,files = file_data,data = post_data,proxies ={'http':'127.0.0.1:8888'})  
	rt_dict= demjson.decode(rsp.text)
	print (rt_dict)  


if __name__ =='__main__':
	uploadFile("123456789")