from typing import List

from bs4 import BeautifulSoup

class FORMAT_TYPE_ENUM(object):
    TITLE = 'TITLE'
    MSG = 'MSG'
    PRICE = 'PRICE'

class Item591(object):
    def __init__(self) -> None:
        self.title = ''
        self.msg = ''
        self.url = ''
        self.price = 0
        self.price_str = ''
        
class Parser591(object):
    def __init__(self) -> None:
        self.item_lt = [] # type: List['Item591']

    def parseHtml_rentItem(self,html_str:str):
        soup = BeautifulSoup(html_str, 'html5lib')
        itemTitle_soup = soup.find('div', class_='item-title')
        itemMessmager_soup = soup.find('div', class_='item-msg')
        itemPrice_soup = soup.find('div', class_='item-price')
        itemURL = soup.a['href']

        self._item = Item591()
        self.formatRentItem_title(itemTitle_soup.text)
        self.formatRentItem_messenger(itemMessmager_soup.text)
        self.formatRentItem_price(itemPrice_soup.text)
        self._item.url = itemURL
        self.item_lt.append (self._item)
    
    def printItemList(self):
        for _item in self.item_lt:
            print(f'{_item.title} - {_item.price} - {_item.msg} - {_item.url}')

    def formatRentItem_title(self,parse_str:str):
        self._item.title = parse_str.split('\n')[1].strip()
    def formatRentItem_messenger(self,parse_str:str):
        self._item.msg = parse_str.split('\n')[1].strip()
    def formatRentItem_price(self,parse_str:str):
        self._item.price_str = parse_str
        self._item.price = int(parse_str.strip().replace('元/月','').replace(',',''))