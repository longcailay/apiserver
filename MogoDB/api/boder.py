import pandas as pd
import json
import difflib
from flask import request, jsonify, make_response, Blueprint
from unidecode import unidecode
import connectionDB as connDB
boder = Blueprint('boder', __name__)


nameDB = 'SuccessfullLand_DB'


#tạo kết nối tới DB và trả ra collection
def collection(nameColl):
    db = connDB.connectionDBAtlas2(nameDB)
    coll = db[nameColl]
    return coll

@boder.errorhandler(404)
def page_not_found():
    data = {
            "statusCode": 404,
            "error": "Not Found",
            "message": "The resource could not be found."
        }
    return json.dumps(data), 404

@boder.errorhandler(500)
def internal_server_error():
    data = {
            "statusCode": 500,
            "error": "Internal Server Error",
            "message": "The server has encountered a situation it doesn't know how to handle."
        }
    return json.dumps(data), 500


#tìm kiếm boder của khu vực
"""
    input: Get: http://127.0.0.1:5000/boder/search
        Params: 
            fullAddress: full address của khu vực
            type: 1 | 2 | 3 => tương ứng tỉnh, huyện, xã
            provinceCode:  vd: ho-chi-minh
            districtCode: quan-1
            villageCode: phuong-3
           


    output: Boder khu vực cần hiển thị cùng center point của khu vực đó

"""
@boder.route('/boder/search', methods=['GET'])
def search():
    try:
        query_parameters = request.args

        FullAddress = query_parameters.get('fullAddress')
        Type = query_parameters.get('type')
        # ProvinceCode = query_parameters.get('provinceCode')
        # DistrictCode = query_parameters.get('districtCode')
        # VillageCode = query_parameters.get('villageCode')

        if not (FullAddress or Type):
            return page_not_found()

        if str(Type) == '1':
            coll = collection('boder_province')
            df = pd.DataFrame(list(coll.find({"properties.NAME_1": FullAddress})))


        # q = q.replace('Tỉnh ','').replace('tỉnh ','')
        # q = formatQuery(q)
        # coll = collection()
        # df = pd.DataFrame(list(coll.find({})))
        # temp = difflib.get_close_matches(q, df['fullAddressCode'])
        # df = pd.DataFrame(list(coll.find({'fullAddressCode': temp[0]})))
        if df.empty:
            data = []
            return json.dumps(data), 200
        else:
            df = df.drop(columns='_id')
            temp = df.to_json(orient='records', force_ascii=False)
            print('HHHHHHH')
            print(type(temp))
            parsed = json.loads(temp)
            print(type(parsed[0]))
            print(parsed[0].get('type'))
            data =  json.dumps(parsed, indent=4, ensure_ascii=False)
            response = make_response(data)
            response.headers['Content-Type'] = 'application/json'
        
            return  response
    except:
        return internal_server_error()
