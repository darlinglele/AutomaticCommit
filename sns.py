# -*- coding: utf-8 -*-
import boto
import boto.sns
from datetime import datetime
import history
def send_ok():
	sns =boto.sns.connect_to_region('ap-northeast-1')
	topics = sns.get_all_topics()["ListTopicsResponse"]["ListTopicsResult"]["Topics"]
	mytopic  = topics[0]
	msg = u"Boss:\n  Everything is ready !"
	print datetime.now().month, datetime.now().day
	msg+=u'\n\n\n\n\n'+ history.history(datetime.now().month,datetime.now().day).string
	subj = "成功完成等保申报任务"
	res = sns.publish(mytopic['TopicArn'], msg, subj)

#send_ok()

# print datetime.datetime.now()
