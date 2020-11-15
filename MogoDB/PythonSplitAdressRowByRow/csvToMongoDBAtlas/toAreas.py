import pandas as pd
import json
import sys
import requests
import ast
sys.path.insert(0, './../Connection')
from pymongo import ASCENDING, DESCENDING
import connectionDB as connDB #Lỗi import cũng không sao
nameDB = 'SuccessfullLand_DB'
nameColl = 'areas'

#tạo collection vào trong database
db = connDB.connectionDBAtlas(nameDB)
collection = db[nameColl]

      
#add thêm tỉnh vào areas
# {
#     Id: ...,
#     fullAddress: 'Hồ Chí Minh',
#     type: 1,
#     provinceCode: 'ho-chi-minh',
#     districtCode: '',
#     villageCode: ''
# }

def addProvinceAreas():
    res = requests.get('http://127.0.0.1:5000/areas')
    dict_str = res.content.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    for dict in mydata:
        result = {}#để ra ngoài thì result sẽ dùng chung cái index
        result['fullAddress'] = dict['province']
        result['type'] = 1
        result['provinceCode'] = dict['provinceCode']
        result['districtCode'] = ''
        result['villageCode'] = ''
        collection.insert_one(result)


def addDistrictAreas():
    res = requests.get('http://127.0.0.1:5000/areas')
    dict_str = res.content.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    for dict in mydata:
        print(type(dict['provinceCode']))
        res2 = requests.get('http://127.0.0.1:5000/areas/'+dict['provinceCode'])
        dict_str2 = res2.content.decode("UTF-8")
        mydata2 = ast.literal_eval(dict_str2)
        for dict2 in mydata2:
            result = {}#để ra ngoài thì result sẽ dùng chung cái index
            result['fullAddress'] = dict2['district'] + ", " + dict['province']
            result['type'] = 2
            result['provinceCode'] = dict['provinceCode']
            result['districtCode'] = dict2['districtCode']
            result['villageCode'] = ''
            collection.insert_one(result)


def addVillageAreas():
    res = requests.get('http://127.0.0.1:5000/areas')
    dict_str = res.content.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    for dict in mydata:
        print(dict['provinceCode'])
        res2 = requests.get('http://127.0.0.1:5000/areas/'+dict['provinceCode'])
        dict_str2 = res2.content.decode("UTF-8")
        mydata2 = ast.literal_eval(dict_str2)
        for dict2 in mydata2:
            print(dict['provinceCode'] + " - " + dict2['districtCode'])
            res3 = requests.get('http://127.0.0.1:5000/areas/'+dict['provinceCode']+"/"+dict2['districtCode'])
            dict_str3 = res3.content.decode("UTF-8")
            mydata3 = ast.literal_eval(dict_str3)
            for dict3 in mydata3:
                result = {}#để ra ngoài thì result sẽ dùng chung cái index
                result['fullAddress'] = dict3['village'] + ", " + dict2['district'] + ", " + dict['province']
                result['type'] = 3
                result['provinceCode'] = dict['provinceCode']
                result['districtCode'] = dict2['districtCode']
                result['villageCode'] = dict3['villageCode']
                collection.insert_one(result)





#Xoa du lieu collection hien tai
collection.delete_many({})
addProvinceAreas()
#collection.create_index([("provinceCode", 1),("districtCode",1)])

addDistrictAreas()
addVillageAreas()


