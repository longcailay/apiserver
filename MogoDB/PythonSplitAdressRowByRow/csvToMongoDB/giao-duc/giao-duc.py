import pandas as pd
import csv
import json
import sys
sys.path.insert(0, './../../Connection')

name = 'giao-duc' #ta lấy tên file csv làm tên cho DB 

import connectionDB as connDB #Lỗi import cũng không sao

#tạo collection vào trong database name
db = connDB.connectionDB('','', 'Utility')
collection = db[name]
collection.delete_many({})
#/#

#import mongoDB from csv
df = pd.read_csv('./'+ name +'.csv')
#apply một thao tác trên một cột của dataframe
df['gps'] = df.apply(lambda row: json.loads(row['gps']), axis = 1)#chuyển gps string sang json

#ghi hết tất cả thông tin của giáo dục trên cả nước vào db = 'giao-duc', collection = 'giao-duc'
def exportAllToCollection():
    mongo_dict = json.loads(df.drop_duplicates(subset=['hash']).to_json(orient='records', force_ascii=False))
    collection.insert(mongo_dict)#nên dùng insert, không nên dùng save

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

#tách giáo dục từng tỉnh để ghi vào từng collection có tên là tỉnh đó
def exportPartialToCollection():
    #get province list from DB
    db = connDB.connectionDB('','','areas')
    coll = db.areas
    dfPro = pd.DataFrame(list(coll.find({'serial': {'$lte': 63}}))) #get dataframe province


    #import mongoDB from csv
    df = pd.read_csv('./giao-duc.csv')
    #apply một thao tác trên một cột của dataframe
    df['gps'] = df.apply(lambda row: json.loads(row['gps']), axis = 1)#chuyển gps string sang json
    
    db2 = connDB.connectionDB('','','giao-duc')
    for index, row in dfPro.iterrows():
        #tạo collection vào trong database
        collName = str(row['provinceCode'])
        print(collName)
        collection = db2[collName]
        collection.delete_many({})

        dfProvince = df[df["provinceCode"] == collName]
        temp = dfProvince.to_json()
        parsed = json.loads(temp)
        #data =  json.dumps(parsed, indent=4, ensure_ascii=False)

        #print(type(Convert(parsed)))
        #mongo_dict = json.loads(dfProvince.to_json())
        collection.insert(parsed)#nên dùng insert, không nên dùng save


    

if __name__ == "__main__":
    exportAllToCollection()


