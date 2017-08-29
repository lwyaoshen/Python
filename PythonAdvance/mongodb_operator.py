import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
#或
#client = pymongo.MongoClient('localhost'，'27017')

db_name = 'test'
db = client[db_name]

collection_set01 = db['set01']
'''
save() vs insert()
mongodb的save和insert函数都可以向collection里插入数据，但两者是有两个区别
1. save函数实际就是根据参数条件,调用了insert或update函数.如果想插入的数据对象存在,insert函数会报错,而save函数是改变原来的对象;如果想插入的对象不存在,那么它们执行相同的插入操作.这里可以用几个字来概括它们两的区别,即所谓"有则改之,无则加之".
2. insert可以一次性插入一个列表，而不用遍历，效率高， save则需要遍历列表，一个个插入.
'''
record_l = [
{'_id':0,'name': 'zzzzz','age': -27,'high': 176},
{'_id':1,'name': 'zhangweijian','age': 27,'high': 171},
{'_id':2,'name': 'zhang','age': 26,'high': 173},
{'_id':3,'name': 'wei','age': 29,'high': 180},
{'_id':4,'name': 'weijian','age': 30,'high': 158},
{'_id':5,'name': 'zhangjian','age': 22,'high': 179},
{'_id':6,'name': 'zwj','age': 19,'high': 166},
{'_id':100,'name': 'zwj','age': 19,'list':[2,3,5]},
{'_id':101,'name': 'zwj','age': 19,'list':[{'name':'ys','age':12},{'name':'ys1','age':14}]},
]
try:
    for record in record_l:
        collection_set01.save(record)
        #pass
except pymongo.errors.DuplicateKeyError:
    print('record exists')
except Exception as e:
    print(e)

'''
remove()
delete_one(self, filter, collation=None)
delete_many(self, filter, collation=None)
'''
'''
newinsert1 = {'_id':7,'comment':'test delete'}
newinsert2 = {'_id':8,'comment':'test delete'}
newinsert3 = {'_id':9,'comment':'test delete'}
collection_set01.save(newinsert1)
collection_set01.save(newinsert2)
collection_set01.save(newinsert3)

remove_before = collection_set01.find()
print('delete before')
for obj in remove_before:
    print(obj)

collection_set01.delete_many({'_id':{'$gt':6,'$lt':100}})   #删除所有满足条件的文档,删除_id大于6，小于100
collection_set01.delete_one({'_id':6})   #删除一条满足条件的文档,删除_id=6
#collection_set01.delete_many({}) #删除整个集合
remove_after = collection_set01.find()
print('delete after')
for obj in remove_after:
    print(obj)
'''


'''

'''