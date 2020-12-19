import flask
import pandas as pd
import json
from flask import request, jsonify, make_response, Blueprint
import connectionDB as connDB
giaoDuc = Blueprint('giaoDuc', __name__)

nameDB = 'SuccessfullLand_DB'
nameColl = 'utilities'


#tạo collection vào trong database
db = connDB.connectionDBAtlas(nameDB)
mycoll = db[nameColl]

#df = pd.DataFrame(list(coll.find({}))).drop(columns='_id')



@giaoDuc.route('/giao-duc/<provinceCode>', methods=['GET'])
def provinces(provinceCode):
    dfProvince = pd.DataFrame(list(myColl.find({"provinceCode": provinceCode}))).drop(columns='_id')
    temp = dfProvince.to_json(orient='records', force_ascii=False)
    parsed = json.loads(temp)
    data =  json.dumps(parsed,indent=4, ensure_ascii=False)
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    return  response


@giaoDuc.route('/giao-duc/<provinceCode>/<districtCode>', methods=['GET'])
def districts(provinceCode, districtCode):
    dfDistrict = pd.DataFrame(list(myColl.find({"provinceCode": provinceCode, "districtCode": districtCode}))).drop(columns='_id')
    temp = dfDistrict.to_json(orient='records', force_ascii=False)
    parsed = json.loads(temp)
    data =  json.dumps(parsed,indent=4, ensure_ascii=False)
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    return  response


@giaoDuc.route('/giao-duc/<provinceCode>/<districtCode>/<villageCode>', methods=['GET'])
def villages(provinceCode, districtCode,villageCode):
    dfDistrict = pd.DataFrame(list(myColl.find({"provinceCode": provinceCode, "districtCode": districtCode, "villageCode":villageCode}))).drop(columns='_id')
    temp = dfDistrict.to_json(orient='records', force_ascii=False)
    parsed = json.loads(temp)
    data =  json.dumps(parsed,indent=4, ensure_ascii=False)
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    return  response
 



