from bs4 import BeautifulSoup
import urllib2
def history(month,day):
	url ='https://zh.wikipedia.org/w/api.php?action=query&titles='+str(month)+'%E6%9C%88'+str(day)+'%E6%97%A5&format=xml&prop=revisions&rvprop=content'
	response= urllib2.urlopen(url).read()
	y=BeautifulSoup(response)
	return y.api.query.pages.page.revisions.rev
