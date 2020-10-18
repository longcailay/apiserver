import flask
import pandas as pd
import json
import csv
from flask import request, jsonify, make_response, Blueprint

giaoDuc = Blueprint('giaoDuc', __name__)


df = pd.read_csv('./data/giao-duc.csv')
#apply một thao tác trên một cột của dataframe
df['gps'] = df.apply(lambda row: json.loads(row['gps']), axis = 1)#chuyển gps string sang json
#dfProvince = df.loc[df["provinceID"] <= 999, ["province","provinceID","provinceCode"]]#tạo subDataframe từ df có 3 cột với điều kiện serial trong df <= 63


@giaoDuc.route('/giao-duc/<provinceCode>', methods=['GET'])
def provinces(provinceCode):
    dfProvince = df[df["provinceCode"] == provinceCode]
    temp = dfProvince.to_json(orient='records', force_ascii=False)
    parsed = json.loads(temp)
    data =  json.dumps(parsed, indent=4, ensure_ascii=False)
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    return  response


@giaoDuc.route('/giao-duc/<provinceCode>/<districtCode>', methods=['GET'])
def districts(provinceCode, districtCode):
    dfProvince = df[ (df["provinceCode"] == provinceCode) & (df["districtCode"] == districtCode)]
    temp = dfProvince.to_json(orient='records', force_ascii=False)
    parsed = json.loads(temp)
    data =  json.dumps(parsed, indent=4, ensure_ascii=False)
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    return  response


@giaoDuc.route('/giao-duc/<provinceCode>/<districtCode>/<villageCode>', methods=['GET'])
def villages(provinceCode, districtCode,villageCode):
    dfProvince = df[ (df["provinceCode"] == provinceCode) & (df["districtCode"] == districtCode) & (df["villageCode"] == villageCode) ]
    temp = dfProvince.to_json(orient='records', force_ascii=False)
    parsed = json.loads(temp)
    data =  json.dumps(parsed, indent=4, ensure_ascii=False)
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    return  response
 



