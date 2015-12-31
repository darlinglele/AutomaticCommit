#-*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib, urllib2, cookielib, time, random
import sns
import datetime
import logging



def get_update_urls(opener):
	list_url= 'http://www.bjdjbh.com/reportinfo/unit/list.do'
	post_data_dictionary ={'pageNum':1,'numPerPage':80,'orderField':'','orderDirection':'','name':''}
	post_data_encoded = urllib.urlencode(post_data_dictionary)
	request_object = urllib2.Request(list_url, post_data_encoded)
	response = opener.open(request_object)
	soup= BeautifulSoup(response,'html.parser')
	links=[]

	for link in soup.findAll('a'):
		if 'sys_normal' in link['href']:
			links.append(link['href'])
	return links


def try_to_update():
	try:
		logging.info(str(datetime.datetime.now())+'try to login...')
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		resp = opener.open('http://www.bjdjbh.com/reportinfo/jsp/login.jsp')
		opener.open('http://www.bjdjbh.com/reportinfo/jsp/valiCod/valiCode.jsp')

		url = "http://www.bjdjbh.com/reportinfo/j_spring_security_check"
		#place POST data in a dictionary
		post_data_dictionary = {'j_username':11930843018, "j_password":'934b0e79d5e10601afe3ee1e5c811707', "valiCode":5}

		post_data_encoded = urllib.urlencode(post_data_dictionary)

		request_object = urllib2.Request(url, post_data_encoded)
	except Exception, e:
		logging.exception('error when try to loign...')
		return False	 
	
	#make the request using the request object as an argument, store response in a variable
	try:
		response = opener.open(request_object)
		string_html = response.read();
		if '退出' in string_html:
			links= get_update_urls(opener)
			logging.info(str(datetime.datetime.now())+'-- check if need to update:')
			if	len(links) == 0:
				logging.info('no items to update!')
				return True
			# update
			logging.info('updating....')
			for link in links:
				logging.info(str(datetime.datetime.now()) + '--'+ link)
				request_object = urllib2.Request(link)
				response = opener.open(request_object)
				time.sleep(random.random()*5)

			if len(get_update_urls(opener)) == 0:
				logging.info(str(datetime.datetime.now())+'all ' + str(len(links))+' has been updated!')
				sns.send_ok()
				return True
			else:
				return False
		else:
			logging.info('login failed...')
			return False
	except Exception, e:
		logging.exception('error when doing update')
		return False



logging.basicConfig(filename='log.txt',level=logging.INFO)


while True:	
	updated = try_to_update()
	time.sleep(3600*10 if updated else random.random()*100)
