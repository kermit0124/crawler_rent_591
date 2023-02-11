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
    update_date = Column('update_date', Integer)


class DiffField(object):
    def __init__(self,fieldName,beforeValue,afterValue) -> None:
        self.fieldName = fieldName
        self.beforeValue = beforeValue 
        self.afterValue = afterValue

class DiffContainer(object):
    def __init__(self) -> None:
        self.rentItem = None
        self.diffField_lt = [] # type: list[DiffField]
    
    def appendDiffField(self,diffField: DiffField):
        self.diffField_lt.append(diffField)

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
    
    def compareIsIdentical(self,rentItemAfter: RentItem,rentItemBefore: RentItem):
        assert type(rentItemAfter) == type(rentItemBefore)
        check_res = True
        # check_res = False if (rentItemAfter.title != rentItemBefore.title) else check_res
        # check_res = False if (rentItemAfter.msg != rentItemBefore.msg) else check_res
        # check_res = False if (rentItemAfter.price != rentItemBefore.price) else check_res

        _LT = ['title','msg','price']
        self.diffField_lt = []
        DIFF_DICT_KEY__BEFORE = 'before'
        DIFF_DICT_KEY__AFTER = 'after'
        DIFF_DICT_KEY__RENTITEM = 'RentItem'
        fieldDiff_dict = {}
        self.diffContainer = DiffContainer()
        self.diffContainer.rentItem = rentItemAfter
        for _fieldName in _LT:
            value1 = getattr(rentItemAfter,_fieldName)
            value2 = getattr(rentItemBefore,_fieldName)
            if (value1 != value2):
                diff_dict = {}
                diff_dict[DIFF_DICT_KEY__BEFORE] = value2
                diff_dict[DIFF_DICT_KEY__AFTER] = value1
                diff_dict[DIFF_DICT_KEY__RENTITEM] = rentItemAfter
                fieldDiff_dict[_fieldName] = diff_dict
                self.fieldDiff_dict = fieldDiff_dict

                diffField = DiffField(_fieldName,value2,value1)
                check_res = False
                self.diffField_lt.append(diffField)

                diffField.afterValue = value1
                diffField.beforeValue = value2
                diffField.fieldName = _fieldName
                self.diffContainer.appendDiffField(diffField)

        return check_res

    def updateOrAppend(self,rentItem_lt: list[RentItem]):
        assert type(rentItem_lt) == type([])
        updateRentItem_new_lt = []
        self.updateDiffContainer_lt = [] # type: list[DiffContainer]
        # updateRentItem_updated_diffField_lt = []
        updateRentItem_updated_diffFieldDict_lt = []
        for _updateRentItem_web in rentItem_lt:
            qRes = self.queryRentItem(RentItem.url == _updateRentItem_web.url)
            if (self.queryResultLen>0):
                for _updateRentItem_qRes in qRes:
                    if (not(self.compareIsIdentical(_updateRentItem_web,_updateRentItem_qRes))):
                        # updateRentItem_updated_diffField_lt.append(self.diffField_lt)
                        updateRentItem_updated_diffFieldDict_lt.append(self.fieldDiff_dict)
                        self.updateDiffContainer_lt.append(self.diffContainer)
                    
                    self.updateQueryResultByRentItem(_updateRentItem_web)
            else:
                updateRentItem_new_lt.append(_updateRentItem_web)
        
        if (updateRentItem_new_lt != []):
            self.addNewRow(updateRentItem_new_lt)

        self.updateRentItem_new_lt = updateRentItem_new_lt
        self.updateRentItem_updated_diffFieldDict_lt = updateRentItem_updated_diffFieldDict_lt
        # self.updateRentItem_updated_diffField_lt = updateRentItem_updated_diffField_lt

    def addNewRow(self,rentItem_or_list: RentItem|list):
        if (type(rentItem_or_list) != type([])):
            rentItem_or_list = [rentItem_or_list]
        
        self.session.add_all(rentItem_or_list)
        self.session.commit()
    
    def updateQueryResultByRentItem(self,rentItem: RentItem):
        update_dict = {}
        update_dict['title'] = rentItem.title
        update_dict['msg'] = rentItem.msg
        update_dict['price'] = rentItem.price
        update_dict['price_str'] = rentItem.price_str
        update_dict['update_date'] = rentItem.update_date
        self.updateQueryResult(update_dict)

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
    # dbOp = Database_wrapper()
    # dbOp.testFlow()
    print('finish')

if __name__ == '__main__':
    test()