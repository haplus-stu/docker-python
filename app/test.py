from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import csv

chrome_path = '/usr/bin/chromium-browser'
chromedriver_path = '/usr/lib/chromium/chromedriver'
o = Options()
o.binary_location = '/usr/bin/chromium-browser'
o.add_argument('--headless')
o.add_argument('--disable-gpu')
o.add_argument('--no-sandbox')
o.add_argument('--window-size=1200x600')

"""
Sample test
"""
d = webdriver.Chrome(chromedriver_path, options=o)
url = 'https://books.rakuten.co.jp/calendar/001001/weekly/?tid=2020-05-18'
d.get(url)

# html = d.page_source

# soup = BeautifulSoup(html,"html.parser")

f = open("output.csv","w")
date_f = open("output_date.csv","w")
link_f = open("output_link.csv","w")


title_list = []
date_list =[]
link_list =[]

page_num = 0
while True:
    html = d.page_source 
    soup = BeautifulSoup(html,"html.parser")

    print("######################page: {0} url: {1} ########################".format(page_num,d.current_url))
    print("Starting to get posts...")
    bk_title = [i.get_text() for i in  soup.select("[class='item-title__text']")]
    date = [i.get_text() for i in soup.select("[class='item-release__date']")]
    link = [tag.get('href') for tag in soup.select("[class='item-title'] a")]


    print(len(bk_title))
    print(len(date))
    print(len(link))
    #print(len(page_li)) 


    for i in range(len(bk_title)):
        title_list.append([bk_title[i]])
        date_list.append([date[i].strip()])
        link_list.append([link[i]])

    if page_num>=2 and len(soup.select("span.inactive"))>0:
        print('page no longer exist')
        break

    next_url_origin = soup.find(".rbcomp__pager-controller > a")
    print(next_url_origin)
    next_url = next_url_origin.find('span').decompose()
    d.get(next_url)
    page_num+=1
    d.implicitly_wait(10)
    print("Moving to next page")
    time.sleep(10)


writecsv = csv.writer(f,lineterminator='\n')
write_date_csv = csv.writer(date_f,lineterminator='\n')
write_link_csv = csv.writer(link_f,lineterminator='\n')

writecsv.writerows(title_list)
write_date_csv.writerows(date_list)
write_link_csv.writerows(link_list)
f.close()
d.quit()
