```
本工程是wehub_callback项目中关于"回调接口"的简易demo,通过python flask框架搭建http服务,来实现回调接口的功能和文件上传的功能

环境配置:   
  python 3
所需要的python库:
  demjson
  flask
  requests

服务端程序: server.py    
	wehub_api(): 处理基本的业务逻辑(实现回调接口的功能)   
	upload_file(): 处理文件上传的逻辑(实现文件上传接口的功能)

测试程序:   
  client.py    
  	演示向回调接口发送业务请求
  uploadFile.py    
    演示文件上传的基本逻辑


请把const.py中的SECRET_KEY 换成自己的key,请把TEST_WXID 改成自己的测试小号,并且自行修改代码中的测试逻辑,

服务器运行在 http://localhost:5678/ 
设置回调接口地址为 http://localhost:5678/wehub_api
文件上传地址为 http://localhost:5678/upload_file

文本消息中静态表情转义对照表:http://wxbs.oss-cn-hangzhou.aliyuncs.com/wehub/Emoji/emoji_index.html
```