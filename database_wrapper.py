from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer, String, DATETIME
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# DB_FILE = 'test.db'
DB_FILE = 'db.db'


""" DON'T MODIFY -> """
RENT_ITEM_TABLE_NAME = 'rent_table'
""" DON'T MODIFY <- """
class RentItem(declarative_base()):
    __tablename__ = RENT_ITEM_TABLE_NAME
    
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    msg = Column('msg', String)
    price = Column('price', Integer)
    price_str = Column('price_str', String)
    url = Column('url', String)
    update_date = Column('update_date', DATETIME)

class Database_wrapper(object):
    def __init__(self) -> None:
        self.engine = create_engine(f'sqlite:///{DB_FILE}', echo=True) # 建立連線
        self.conn = self.engine.connect()
        self.db = MetaData() # 取得類似於 Cursor 的物件
        self.session = sessionmaker(bind=self.engine)()
        self.__initDb_rentTable()
        self.queryResult = self.session.query()
        self.queryResultLen = 0
        self.queryResultList = []
    
    def __initDb_rentTable(self):
        """ Try to create the table """
        RentItem.metadata.create_all(self.engine)
    
    def addNewRow(self,rentItem_or_list: RentItem|list):
        if (type(rentItem_or_list) != type([])):
            rentItem_or_list = [rentItem_or_list]
        
        self.session.add_all(rentItem_or_list)
        self.session.commit()
    
    def updateQueryResult(self,update_dict):
        self.queryResult.update(update_dict)
        self.session.commit()

    def queryRentItem(self,alchemyFilter_or_list = None):
        qRes = self.session.query(RentItem)
        if (type (alchemyFilter_or_list) == type([])):
            for af in alchemyFilter_or_list:
                qRes = qRes.filter(af)
        elif (type(alchemyFilter_or_list) == type(None)):
            """ query all data without any filiter """
        else:
            qRes = qRes.filter(alchemyFilter_or_list)
        
        self.queryResultList = []
        for idx, rentItem in enumerate(qRes):
            self.queryResultLen = idx+1
            self.queryResultList.append(rentItem)

        self.queryResult = qRes
        return qRes



    def testFlow(self):
        t = self.queryRentItem()
        t = self.queryRentItem(RentItem.price == 458)
        t = self.queryRentItem([RentItem.price == 458,RentItem.id == 3])
        self.updateQueryResult({'msg':None,'title':'ttttt'})
        t = self.queryRentItem([RentItem.price == 458,RentItem.id == 5])

        t = RentItem()
        t.msg = 'aabcdsssddddd'
        t2 = RentItem()
        t2.msg = '123333'
        self.addNewRow([t,t2])
def test():
    dbOp = Database_wrapper()
    dbOp.testFlow()
    print('finish')

if __name__ == '__main__':
    test()