#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text

from utils import create_wxnr_first,create_wxnr_second,create_wxnr_third,\
				show_completed_weiboxnr,show_uncompleted_weiboxnr,delete_weibo_xnr,\
				continue_create_weiboxnr,create_wxnr_fans,delete_wxnr_fans,\
				wxnr_timing_tasks,wxnr_timing_tasks_lookup,wxnr_timing_tasks_change,wxnr_timing_tasks_revoked,\
				wxnr_list_concerns,wxnr_list_fans


mod = Blueprint('weibo_xnr_manage', __name__, url_prefix='/weibo_xnr_manage')

#test:219.224.134.213:9209/weibo_xnr_manage/create_wxnr_first/?password=1&create_time='2017-07-15 11:30:00'&domain_name='习大大粉丝'&role_name='律师'&psy_feature='中立'&political_side='中立'&business_goal='渗透'&daily_interests='音乐'&monitor_keywords='律师'
@mod.route('/create_wxnr_first/')
def ajax_create_wxnr_first():
	password=request.args.get('password','')
	create_time=request.args.get('create_time','')
	domain_name=request.args.get('domain_name','')
	role_name=request.args.get('role_name','')
	psy_feature=request.args.get('psy_feature','')
	political_side=request.args.get('political_side','')
	business_goal=request.args.get('business_goal','')
	daily_interests=request.args.get('daily_interests','')
	monitor_keywords=request.args.get('monitor_keywords','')
	wxnr_goal_info=[password,create_time,domain_name,role_name,psy_feature,political_side,business_goal,daily_interests,monitor_keywords]  
	results =create_wxnr_first(wxnr_goal_info)
	return results[-1]							#resutls[0]为提示是否创建成功,resutls[-1]返回的是创建虚拟人的id，例如WXNR0001

#test:219.224.134.213:9209/weibo_xnr_manage/create_wxnr_second/?user_id='WXNR0002'&nick_name='律师小绿'&age=25&sex='男'&location='北京'&career='律师'&description='伸张正义，关注和平'&active_time='20,22'&day_post_average='5'
@mod.route('/create_wxnr_second/')
def ajax_create_wxnr_second():
	user_id=request.args.get('user_id','')		#个人中心部分的修改、创建时的下一步等地方可获取user_id进行操作
	nick_name=request.args.get('nick_name','')
	age=request.args.get('age','')
	sex=request.args.get('sex','')
	location=request.args.get('location','')
	career=request.args.get('career','')
	description=request.args.get('description','')
	active_time=request.args.get('active_time','')
	day_post_average=request.args.get('day_post_average','')
	wxnr_role_info=[nick_name,age,sex,location,career,description,active_time,day_post_average]
	results=create_wxnr_second(user_id,wxnr_role_info)
	return json.dumps(results)


#test:219.224.134.213:9209/weibo_xnr_manage/create_wxnr_third/?user_id='WXNR0002'&uid='1440413543'&weibo_mail_count='924202346@qq.com'&weibo_phone_count='15111219660'
@mod.route('/create_wxnr_third/')
def ajax_create_wxnr_third():
	user_id=request.args.get('user_id','')
	uid=request.args.get('uid','')
	weibo_mail_count=request.args.get('weibo_mail_count','')
	weibo_phone_count=request.args.get('weibo_phone_count','')
	wxnr_account_info=[uid,weibo_mail_count,weibo_phone_count]
	results=create_wxnr_third(user_id,wxnr_account_info)
	return json.dumps(results)

#test:http://219.224.134.213:9209/weibo_xnr_manage/show_completed_weiboxnr/
@mod.route('/show_completed_weiboxnr/')
def ajax_show_completed_weiboxnr():
	results=show_completed_weiboxnr()
	return json.dumps(results)

#test:http://219.224.134.213:9209/weibo_xnr_manage/show_uncompleted_weiboxnr/
@mod.route('/show_uncompleted_weiboxnr/')
def ajax_show_uncompleted_weiboxnr():
	results=show_uncompleted_weiboxnr()
	return json.dumps(results)

#test:http://219.224.134.213:9209/weibo_xnr_manage/delete_weibo_xnr/?user_id=WXNR0003
@mod.route('/delete_weibo_xnr/')
def ajax_delete_weibo_xnr():
	user_id=request.args.get('user_id','')
	results=delete_weibo_xnr(user_id)
	return json.dumps(results)

#test:http://219.224.134.213:9209/weibo_xnr_manage/continue_create_weiboxnr/?user_id=WXNR0003
@mod.route('/continue_create_weiboxnr/')
def ajax_continue_create_weiboxnr():
	user_id=request.args.get('user_id','')
	results=continue_create_weiboxnr(user_id)
	return json.dumps(results)


#step 4.2:timing task list
#获取定时发送任务列表
#test:http://219.224.134.213:9209/weibo_xnr_manage/wxnr_timing_tasks/?user_id=WXNR0004
@mod.route('/wxnr_timing_tasks/')
def ajax_wxnr_timing_tasks():
	user_id=request.args.get('user_id','')
	results=wxnr_timing_tasks(user_id)
	return json.dumps(results)

#查看某一具体任务
#test:http://219.224.134.213:9209/weibo_xnr_manage/wxnr_timing_tasks_lookup/?task_id=1234567890_1500108142
@mod.route('/wxnr_timing_tasks_lookup/')
def ajax_wxnr_timing_tasks_lookup():
	task_id=request.args.get('task_id','')
	results=wxnr_timing_tasks_lookup(task_id)
	return json.dumps(results)

#修改某一具体任务
#说明：点击修改这一操作时，首先是执行查看某一具体任务这一功能，然后修改页面内容后，提交时调用该修改函数
#test:http://219.224.134.213:9209/weibo_xnr_manage/wxnr_timing_tasks_change/?task_id=1234567890_1500108142&task_source='日常发帖'&operate_type='origin'&create_time=1500110468&post_time=1500108142&text='明天有一起参加夜跑的吗？我想参加'&remark='待定'
@mod.route('/wxnr_timing_tasks_change/')
def ajax_wxnr_timing_tasks_change():
	task_id=request.args.get('task_id','')      #指_id这个字段
	#对任务具体内容进行修改
	task_source=request.args.get('task_source','')
	operate_type=request.args.get('operate_type','')
	create_time=request.args.get('create_time','')
	post_time=request.args.get('post_time','')
	text=request.args.get('text','')
	remark=request.args.get('remark','')
	task_change_info=[task_source,operate_type,create_time,post_time,text,remark]
	results=wxnr_timing_tasks_change(task_id,task_change_info)
	return json.dumps(results)

#撤销未发送的任务
@mod.route('/wxnr_timing_tasks_revoked/')
def ajax_wxnr_timing_tasks_revoked():
	task_id=request.args.get('task_id','') 
	results=wxnr_timing_tasks_revoked(task_id)
	return json.dumps(results)

#step 4.4: list of concerns
@mod.route('/wxnr_list_concerns/')
def ajax_wxnr_list_concerns(): 
	user_id=request.args.get('user_id','')
	order_id=request.args.get('order_id','')
	results=wxnr_list_concerns(user_id,order_id)
	return json.dumps(results)
 
#step 4.5: list of fans
@mod.route('/wxnr_list_fans/')
def ajax_wxnr_list_fans():
	user_id=request.args.get('user_id','')
	order_id=request.args.get('order_id','')
	results=wxnr_list_fans(user_id,order_id)
	return json.dumps(results)

##########test code ,can be delete##################
#test:http://219.224.134.213:9209/weibo_xnr_manage/create_wxnr_fans/?user_id=WXNR0002&fans_info=[5537979196,3969238480,3302557313,5717296960]
@mod.route('/create_wxnr_fans/')
def ajax_create_wxnr_fans():
	#user_id='WXNR0002'
	#fans_info=[5537979196,3969238480,3302557313,5717296960]
	user_id=request.args.get('user_id','')
	fans_info=request.args.get('fans_info','')
	results=create_wxnr_fans(user_id,fans_info)
	return json.dumps(results)

#test:http://219.224.134.213:9209/weibo_xnr_manage/delete_wxnr_fans/?user_id=WXNR0002
@mod.route('/delete_wxnr_fans/')
def ajax_delete_wxnr_fans():
	user_id=request.args.get('user_id','')
	results=delete_wxnr_fans(user_id)
	return json.dumps(results)



