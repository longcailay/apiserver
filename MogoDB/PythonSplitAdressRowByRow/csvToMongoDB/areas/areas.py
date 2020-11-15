import pandas as pd
import csv
import json
import sys
sys.path.insert(0, './../../Connection')

name = 'areas' #ta lấy tên file csv làm tên cho cả DB và collection 

import connectionDB as connDB #Lỗi import cũng không sao

#tạo collection vào trong database
db = connDB.connectionDB('','', name)
collection = db[name]
collection.delete_many({})
#/#

#import mongoDB from csv
df = pd.read_csv('./'+ name +'.csv')
mongo_dict = json.loads(df.to_json(orient='records', force_ascii=False))
collection.insert(mongo_dict)#nên dùng insert, không nên dùng save
