

本工程是wehub_callback项目中回调接口的demo

环境配置:
  python 3
所需要的python 库
  demjson
  flask
  requests

服务端程序: server.py
	wehub_api(): 处理基本的业务逻辑,实现回调接口的功能
	upload_file(): 处理文件上传的逻辑,实现文件上传接口的功能

测试程序:
  client.py 
  	演示向回调接口发送业务请求
  
  uploadFile.py 
    演示文件上传的基本逻辑
