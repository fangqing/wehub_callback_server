# -*- coding: utf-8 -*-

#当前api文档里支持的actions
ACTIONS =['login','logout','report_contact','report_new_friend','report_new_msg','pull_task','report_task_result','report_room_member_info']

#request格式解析
REQUEST_BASE_CHECK_KEYS = ['action','appid','wxid','data']

#respone格式
RESPONE_BASE_CHECK_KEYS = ['error_code','error_reason','ack_type','data']