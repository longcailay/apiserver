# import pymongo
# #chú ý: database chỉ tạo khi có insert dữ liệu vào database đó
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient['fistDB']
# mydb.mycoll.insert_one({"test": 'test'})
# print(myclient.list_database_names())

#Add folder Connection vào path để khi thực thi trên cmd, các file trong Connection nó cùng
# level với file thực thi
import sys
sys.path.insert(1, './Connection')

#print(sys.path)
import Connection.connectionDB as connDB

connDB = connDB.connectionDB('','','abc')
connDB.mycoll.insert_one({"test": 'testffffff44'})
connDB.mycoll2.insert_one({"test": 'test'})
connDB.myco.insert_one({"test": 'test'})
#connDB.mycoll.delete_many({})



