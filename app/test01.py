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

url ='https://www.amazon.co.jp/s?i=stripbooks&bbn=2278488051&rh=n%3A465392%2Cn%3A465610%2Cn%3A466280%2Cn%3A2278488051%2Cp_6%3AAN1VRQENFRJN5%2Cp_n_publication_date%3A2285539051&dc&qid=1590279932&rnid=82836051&ref=sr_nr_p_n_publication_date_3'

d.get(url)

html = d.page_source

soup = BeautifulSoup(html,"html.parser")

f = open("output.csv","w")
date_f = open("output_date.csv","w")
link_f = open("output_link.csv","w")


title_list = []
date_list =[]
link_list =[]

while True:
    print("######################now-page:{0} ########################".format(d.current_url))
    print("Starting to get posts...")
    bk_title = [i.get_text() for i in  soup.select("[class='a-size-medium a-color-base a-text-normal']")]
    date = [i.get_text() for i in soup.select("[class='a-size-base a-color-secondary a-text-normal']")]
    link = [tag.get('href') for tag in soup.select("[class='a-link-normal a-text-normal']")]


    print(len(bk_title))
    print(len(date))
    print(len(link))



    for i in range(len(bk_title)):
        title_list.append([bk_title[i]])
        date_list.append([date[i].strip()])
        link_list.append(['https://www.amazon.co.jp'+link[i]])

    # page_num+=1
    # btn = soup.find('.a-last')
    if len( soup.select("[class='a-last']"))<0:
        print("no pager exist anymore")
        break
    next_url = [tag.get('href') for tag in soup.select("[class='a-last'] a")]
    print("next url{0}".format(next_url))
    d.get(next_url)
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
