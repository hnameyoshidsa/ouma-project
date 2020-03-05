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
    for m in range(1,13):
        if y == today_year and m > today_month:
            break

        c = calendar.monthcalendar(y, m)
        days = [x[calendar.SUNDAY] for x in c]
        days.extend([x[calendar.SATURDAY] for x in c])

        for d in days:
            url = '/race/list/%d%02d%02d/'%(y,m,d)
            url_list.append((url, '%d%02d%02d'%(y,m,d)))

# タイムアウトを設定
socket.setdefaulttimeout(10)

for url, datestr in url_list:
    driver.get(url_base+url)
    links = driver.find_element_by_css_selector(".db > div#page > div#contents > div#main > div > div a")
    href = links.get_attribute('href')
    if len(href) != 0:
        race_data = [href, datestr]
        race_url_list.append(race_data)

print('list')

with open('race_database-netkeiba.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    print('print')
    for url, datestr in race_url_list:
        driver.get(url)
        print(url[33:35])
        where = ''
        if url[33:35] == '10':
            where = '小倉'
        elif url[33:35] == '09':
            where = '阪神'
        elif url[33:35] == '08':
            where = '京都'
        elif url[33:35] == '07':
            where = '中京'
        elif url[33:35] == '06':
            where = '中山'
        elif url[33:35] == '05':
            where = '東京'
        elif url[33:35] == '04':
            where = '新潟'
        elif url[33:35] == '03':
            where = '福島'
        elif url[33:35] == '02':
            where = '函館'
        elif url[33:35] == '01':
            where = '札幌'
        

    

selenium_close()

