import flask
import pandas as pd
import json
import csv
from flask import request, jsonify, make_response, Blueprint

import connectionDB as connDB
areas = Blueprint('areas', __name__)


db = connDB.connectionDB('','','areas')
coll = db.areas
df = pd.DataFrame(list(coll.find({}))).drop(columns='_id')


#đọc dữ liệu combobox của tỉnh, huyện xã
#df = pd.read_csv('./data/areas.csv')

dfProvince = df.loc[df["provinceID"] <= 999, ["province","provinceID","provinceCode"]]#tạo subDataframe từ df có 3 cột với điều kiện serial trong df <= 63

#load lên danh sách tất cả các tỉnh
@areas.route('/areas', methods=['GET'])
def provinces():
    temp = dfProvince.to_json(orient='records', force_ascii=False)
    parsed = json.loads(temp)
    data =  json.dumps(parsed, indent=4, ensure_ascii=False)
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    return  response

#load lên danh sách tất cả các quận huyện của tỉnh
@areas.route('/areas/<provinceCode>', methods=['GET'])
def districts(provinceCode):
    dfDistrict = df.loc[df["pro_districtCode"] == provinceCode, ["district", "districtID", "districtCode"]] #tạo subDataframe của huyện
    temp = dfDistrict.to_json(orient='records', force_ascii=False)
    parsed = json.loads(temp)
    data =  json.dumps(parsed, indent=4, ensure_ascii=False)
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    return  response

#load lên danh sách tất cả các xã của huyện
@areas.route('/areas/<provinceCode>/<districtCode>', methods=['GET'])
def villages(provinceCode, districtCode):
    dfDistrict = df.loc[(df["pro_districtCode"] == provinceCode) & (df["districtCode"] == districtCode), ["districtID", "districtCode"]] #tạo subDataframe của huyện 
    districtID = int(dfDistrict['districtID'].values[0])
    dfVillage = df.loc[df["dis_villageID"] == districtID, ["village", "villageID", "villageCode","dis_villageCode","dis_villageID"]] #tạo subDataframe của xã
    temp = dfVillage.to_json(orient='records', force_ascii=False)
    parsed = json.loads(temp)
    data =  json.dumps(parsed, indent=4, ensure_ascii=False)
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    return  response
 



