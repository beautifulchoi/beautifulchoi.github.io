import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import re
#네이버 오늘 서울 날씨 사이트 접근
url='https://search.naver.com/search.naver?sm=tab_sug.top&where=nexearch&query=%EC%98%A4%EB%8A%98+%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8&oquery=%EB%84%A4%EC%9D%B4%EB%B2%84+%EB%82%A0%EC%94%A8&tqi=hniIJlp0Yihss6xYN%2FossssstO4-003503&acq=%EC%98%A4%EB%8A%98+%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8&acr=1&qdt=0'
headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
res=requests.get(url, headers=headers)
res.raise_for_status()
#날씨 정보 받아오기
soup=BeautifulSoup(res.text, 'lxml')
weather=soup.find('p', attrs={'class':'cast_txt'})
temp=soup.find('p', attrs={'class':'info_temperature'})
tem_ran=soup.find_all('span', attrs={'class':'num'})
low_tem=tem_ran[0]
high_tem=tem_ran[1]
rain_mor=soup.find('li', attrs={'class':'date_info today'}).find_all('span', attrs={'class':'num'})[0]
rain_aft=soup.find('li', attrs={'class':'date_info today'}).find_all('span', attrs={'class':'num'})[1]
#날씨 정보 출력
print(weather.get_text())
print('현재'+temp.get_text().replace('도씨', '')+'(최저: '+low_tem.get_text()+' 최대: '+high_tem.get_text()+')')
print('오전 강수확률: {0}% 오후 강수확률: {1}'.format(rain_mor.get_text(), rain_aft.get_text()))


#헤드라인 뉴스 정보 받아오기
driver=webdriver.Chrome()
url= 'https://news.naver.com'
driver.get(url)
soup=BeautifulSoup(driver.page_source, 'lxml')
headlines=soup.find('ul', attrs={'class':'hdline_article_list'}).find_all('li')
for idx, headline in enumerate(headlines):
    news_link=headline.find('a')['href']
    news_title=headline.find('a').get_text().strip()
    print('{}: {}'.format(idx+1, news_title))
    print('(링크:{})'.format(news_link))
    if '백신' in news_title:
        print('있음')
        driver.get(url+news_link)
        time.sleep(2)
        driver.back()

driver.find_element_by_xpath('//*[@id="lnb"]/ul/li[8]/a').click()

time.sleep(100)