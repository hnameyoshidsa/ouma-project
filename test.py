import re
import socket
import calendar
import datetime
import csv
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

options = FirefoxOptions()
options.add_argument('-headless')
driver = webdriver.Firefox(executable_path='geckodriver.exe',options=options)

# Firefoxで任意のURLを開く
def selenium_get(url):
  driver.get(url)

# Firefoxを閉じる
def selenium_close():
    driver.close()

url_base = 'http://db.netkeiba.com'
url_list = []
race_url_list = []

today_year = datetime.datetime.today().year
today_month = datetime.datetime.today().month

for y in [2019]:
#for y in [2017,2018,2019]:
	for m in range(1,13):
		if y == today_year and m > today_month:
			break

		c = calendar.monthcalendar(y, m)
		days = [x[calendar.SUNDAY] for x in c]
		days.extend([x[calendar.SATURDAY] for x in c])

		for d in days:
			url = '/race/list/%d%02d%02d/'%(y,m,d)
			url_list.append((url, '%d%02d%02d'%(y,m,d)))
		#print(url_list)
		
		#for d in range(1,32):
		#	s = '%d%02d%02d/'%(y,m,d)
		#	if s in holidays:
		#		url = '/race/list/%d%02d%02d/'%(y,m,d)
		#		url_list.append((url, '%d%02d%02d'%(y,m,d)))

# タイムアウトを設定
socket.setdefaulttimeout(10)

for url, datestr in url_list:
    driver.get(url_base+url)
    links = driver.find_element_by_css_selector(".db > div#page > div#contents > div#main > div > div a")
    href = links.get_attribute('href')
    race_data = [(x, datestr) for x in href]
    race_url_list.extend(race_data)
	#レース情報のURLリスト
#driver.save_screenshot("website.png")
selenium_close()
