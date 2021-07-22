from selenium import webdriver
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook
#엑셀 파일 생성
wb=Workbook()
ws=wb.active
ws.append(('영화명', '장르', '별점', '할인정보', '원가격', '현재가격'))

url='https://play.google.com/store/movies/new'
driver=webdriver.Chrome()
driver.maximize_window()
driver.get(url)
#1. 스크롤 끝까지 내리기
pause_time=1
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        print('스크롤 다내림')
        break
    last_height = new_height

#2.영화 정보 받아오기
soup=BeautifulSoup(driver.page_source, 'lxml')
movies=soup.find_all('div', attrs={'class':'vU6FJ p63iDd'})
for movie in movies:
    title=movie.find('div', attrs={'class':'b8cIId ReQCgd Q9MA7b'}).find('div').get_text()
    genre=movie.find('div', attrs={'class':'KoLSrc'})
    rate=movie.find('div', attrs={'class':'pf5lIe'})
    if rate and genre:
        rate=rate.div['aria-label']
        genre=genre.get_text()
        #print(title, genre, rate)
    elif rate:
        rate=rate.div['aria-label']
        #print(title)
        
    elif genre:
        genre=genre.get_text()
        rate='평점 없음'
        
    else:
        genre='장르 없음'
        rate='평점 없음'
    
    cur_price=movie.find('span', attrs={'class':'VfPpfd ZdBevf i5DZme'})
    ori_price=movie.find('span',attrs={'class':'SUZt4c djCuy'})
    if ori_price==None:
        discount='할인 영화 아님'
        ori_price=cur_price
    else:
        discount='할인 영화'

    ws.append((title, genre, rate, discount,ori_price.get_text(),cur_price.get_text()))

wb.save("최신영화목록.xlsx")    
time.sleep(10)