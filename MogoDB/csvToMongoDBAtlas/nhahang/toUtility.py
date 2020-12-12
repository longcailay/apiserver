import pandas as pd
import csv
import json
import sys
sys.path.insert(0, './../../Connection')
import ast
from pymongo import ASCENDING, DESCENDING
import connectionDB as connDB #Lỗi import cũng không sao
nameDB = 'SuccessfullLand_DB'
nameColl = 'utilities'

name = 'hcm_hospitalOutput' 



#tạo collection vào trong database
db = connDB.connectionDBAtlas(nameDB)
collection = db[nameColl]

#import mongoDB from csv
df = pd.read_csv('./'+ name +'.csv')
#apply một thao tác trên một cột của dataframe
df['gps'] = df.apply(lambda row: json.loads(row['gps']), axis = 1)#chuyển gps string sang json
print(type(df))

#ghi hết tất cả thông tin của giáo dục trên cả nước vào collection
def exportAllToCollection():
    mongo_dict = json.loads(df.drop_duplicates(subset=['hash']).to_json(orient='records', force_ascii=False))
    for dict in mongo_dict:
        print(dict)
        result = {}
        result['title'] = dict['title']
        result['fullAddress'] = dict['address']
        result['category'] = dict['category']
        result['img'] = dict['img']
        result['imgBig'] = dict['img_big']
        result['phone'] = dict['phone']
        result['email'] = dict['email']
        result['facebook'] = dict['facebook']
        result['gps'] = dict['gps']
        result['village'] = dict['village']
        result['district'] = dict['district']
        result['province'] = dict['province']
        result['villageCode'] = dict['villageCode']
        result['districtCode'] = dict['districtCode']
        result['provinceCode'] = dict['provinceCode']
        result['street'] = dict['street']
        result['streetCode'] = dict['streetCode']
        result['areas'] = [
            dict['province'],
            dict['district'] + ", " + dict['province'],
            dict['village'] + ", " + dict['district'] + ", " + dict['province']
        ]
        collection.insert_one(result)
    #collection.insert(mongo_dict)#nên dùng insert, không nên dùng save


if __name__ == "__main__":
    exportAllToCollection()