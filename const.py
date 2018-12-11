# -*- coding: utf-8 -*-

BIND_HOST = 'localhost'
BIND_PORT = 5678

#当前api文档里支持的actions,可能会持续增加
ACTIONS =['login','logout','report_contact','report_new_friend','report_new_msg','pull_task','report_task_result','report_room_member_info','report_room_member_change']

#request格式解析
REQUEST_BASE_CHECK_KEYS = ['action','appid','wxid','data']

#respone格式
RESPONE_BASE_CHECK_KEYS = ['error_code','error_reason','ack_type','data']

MSG_TYPE_INVALID = 0
MSG_TYPE_TEXT = 1
MSG_TYPE_IMAGE = 3	#图片
MSG_TYPE_LINK = 49
MSG_TYPE_VOICE = 0x22	#音频
MSG_TYPE_VIDEO = 0x2B	#视频
MSG_TYPE_FILE = 4903    #文件

'''这些类型的消息里需要上传文件'''
UPLOADFILE_MSG_TYPES = [MSG_TYPE_IMAGE,MSG_TYPE_VOICE,MSG_TYPE_VIDEO,MSG_TYPE_FILE]

TASK_TYPE_SENDMSG = 1  		#发消息
TASK_TYPE_KICK = 2  		#踢人
TASK_TYPE_INVITE_ROOM = 3	#发入群邀请
TASK_TYPE_REPORT_ROOMMEMBER = 4  #上报群成员信息
TASK_TYPE_ADD_ROOMMEMBER_FRIEND = 5    #加群成员为好友
TASK_TYPE_REMARK_FRIEND = 6
TASK_TYPE_CHANGE_ROOM_NICKNAME = 7
TASK_TYPE_QUIT_ROOM = 8
TASK_TYPE_UPLOAD_FILE = 9

FIX_REQUEST_TYPES = ['login','logout','pull_task']
SECRET_KEY = "eovBCOX3457@"    #换成自己的secret_key
TEST_WXID = "wxid_hrtv4z7etgvc22"    #换成自己的测试小号
UPLOAD_FOLDER = 'd:/test_uploads'     #上传的文件的存放地址,换成服务端的文件存储路径