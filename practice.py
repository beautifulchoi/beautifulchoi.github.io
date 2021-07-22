import requests
from bs4 import BeautifulSoup
import csv

url = 'https://finance.naver.com/sise/sise_market_sum.nhn?&page=1'
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
res= requests.get(url, headers=headers)
res.raise_for_status()
f = open('코스피.csv', 'w', encoding='utf-8-sig', newline='')
wr = csv.writer(f)
soup=BeautifulSoup(res.text, 'lxml')
data_rows=soup.find('tbody').find_all('tr', attrs={'onmouseover':'mouseOver(this)'})
titles=soup.find('thead').find_all('th')
title_data=[title.get_text() for title in titles]
wr.writerow(title_data)
for row in data_rows:
    columns=row.find_all('td')
    data=[column.get_text().strip() for column in columns]
    wr.writerow(data)


f.close()
