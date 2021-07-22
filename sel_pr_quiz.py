from selenium import webdriver
import time
#1. 브라우저 접속
url='https://www.w3schools.com/'
browser=webdriver.Chrome()
browser.get(url)
#2. Learn html 클릭
browser.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[1]/a[1]').click()
#3.how to 클릭
browser.find_element_by_xpath('//*[@id="topnav"]/div/div/a[10]').click()
#4.contact form 메뉴 클릭
browser.find_element_by_xpath('//*[@id="leftmenuinnerinner"]/a[contains(text(), "Contact")]').click()
#5.입력란에 값 입력
browser.find_element_by_xpath('//*[@id="fname"]').send_keys('나도')
browser.find_element_by_xpath('//*[@id="lname"]').send_keys('코딩')
browser.find_element_by_xpath('//*[@id="country"]/option[2]').click()
browser.find_element_by_xpath('//*[@id="main"]/div[3]/textarea').send_keys('완료')
time.sleep(2)
browser.find_element_by_xpath('//*[@id="main"]/div[3]/a').click()
time.sleep(2)
browser.quit()