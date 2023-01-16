from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from parser_591 import Parser591

# START_URL = 'https://rent.591.com.tw/?kind=1&region=1&section=11,4,7&searchtype=1&rentprice=,30000&multiRoom=2,3,4&showMore=1&order=money&orderType=asc&multiNotice=not_cover&keywords=%E6%B0%B8%E5%90%89'
# START_URL = 'https://rent.591.com.tw/?kind=1&region=1&section=11,4,7&searchtype=1&rentprice=,30000&multiRoom=2,3,4&showMore=1&order=money&orderType=asc&multiNotice=not_cover&firstRow=0&totalRows=193'
START_URL = 'https://rent.591.com.tw/?keywords=%E4%BF%A1%E7%BE%A9%E8%B7%AF%E5%85%AD%E6%AE%B5&order=money&orderType=asc' # test: 2pages
WAIT_LOAD_TIME_SEC = 1



parser591 = Parser591()

options = Options()
options.add_argument("--disable-notifications")

chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
chrome.get(START_URL)

driver = chrome
newPage = True
pageCnt = 0
while(newPage):
    time.sleep(WAIT_LOAD_TIME_SEC)
    nextPage_button = driver.find_elements(By.CLASS_NAME,'pageNext')
    eles = driver.find_elements(By.CLASS_NAME,"vue-list-rent-item")

    for _ele in eles:
        try:
            html = _ele.get_attribute('innerHTML')
            parser591.parseHtml_rentItem(html)
        except:
            print('Get html error')
    
    _btn = nextPage_button[0]
    if (_btn.aria_role == 'link'):
        _btn.click()
    else:
        newPage = False

    print(f'Page:{pageCnt} - got items:{len(eles)}')
    pageCnt += 1
parser591.printItemList()

#print(driver.get_attribute('innerHTML'))


#email = chrome.find_element_by_id("email")
#password = chrome.find_element_by_id("pass")
 
#email.send_keys('')
#password.send_keys('')
#password.submit()