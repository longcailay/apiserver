import flask
import pandas as pd
import json
import csv
import difflib
from flask import request, jsonify, make_response, Blueprint

import connectionDB as connDB
areas = Blueprint('areas', __name__)


nameDB = 'SuccessfullLand_DB'
nameColl = 'areas'


#tạo kết nối tới DB và trả ra collection
def collection():
    db = connDB.connectionDBAtlas(nameDB)
    coll = db[nameColl]
    return coll

@areas.errorhandler(404)
def page_not_found():
    return "<h1>404 Not Found</h1><p>The resource could not be found.</p>", 404

@areas.errorhandler(500)
def internal_server_error():
    return "<h1>500 Internal Server Error</h1><p>The server has encountered a situation it doesn't know how to handle.</p>", 500

#load lên danh sách tất cả các tỉnh
"""
    input: Get: http://127.0.0.1:5000/areas
    output: danh sách 63 tỉnh của cả nước

"""
@areas.route('/areas', methods=['GET'])
def provinces():
    try:
        coll = collection()
        df = pd.DataFrame(list(coll.find({"type": 1})))
        if df.empty:
            return page_not_found()
        else:
            df = df.drop(columns='_id')
            temp = df.to_json(orient='records', force_ascii=False)
            parsed = json.loads(temp)
            data =  json.dumps(parsed, indent=4, ensure_ascii=False)
            response = make_response(data)
            response.headers['Content-Type'] = 'application/json'
            return  response
    except:
        return internal_server_error()
#load lên danh sách tất cả các quận huyện của tỉnh
"""
    input: Get: http://127.0.0.1:5000/areas/ho-chi-minh
    output: danh sách tất cả các quận huyện ở thành phố Hồ Chí Minh

"""
@areas.route('/areas/<provinceCode>', methods=['GET'])
def districts(provinceCode):
    try:
        coll = collection()
        df = pd.DataFrame(list(coll.find({"type": 2, "provinceCode": provinceCode})))
        if df.empty:
            return page_not_found()
        else:
            df = df.drop(columns='_id')
            temp = df.to_json(orient='records', force_ascii=False)
            parsed = json.loads(temp)
            data =  json.dumps(parsed, indent=4, ensure_ascii=False)
            response = make_response(data)
            response.headers['Content-Type'] = 'application/json'
            return  response
    except:
        return internal_server_error()

#load lên danh sách tất cả các xã của huyện
"""
    input: Get: http://127.0.0.1:5000/areas/ho-chi-minh/quan-1
    output: danh sách tất cả các phường ở quận 1, thành phố Hồ Chí Minh

"""
@areas.route('/areas/<provinceCode>/<districtCode>', methods=['GET'])
def villages(provinceCode, districtCode):
    try:
        coll = collection()
        df = pd.DataFrame(list(coll.find({"type": 3, "provinceCode": provinceCode, "districtCode": districtCode})))
        if df.empty:
            return page_not_found()
        else:
            df = df.drop(columns='_id')
            temp = df.to_json(orient='records', force_ascii=False)
            parsed = json.loads(temp)
            data =  json.dumps(parsed, indent=4, ensure_ascii=False)
            response = make_response(data)
            response.headers['Content-Type'] = 'application/json'
        
            return  response
    except:
        return internal_server_error()
    

#tìm kiếm khu vực do người dùng nhập vào
"""
    input: Get: http://127.0.0.1:5000/areas/search?q=Thành Phố Hồ Chí Minh
    output: danh sách tất cả các phường ở quận 1, thành phố Hồ Chí Minh

"""
@areas.route('/areas/search', methods=['GET'])
def search():
    try:
        query_parameters = request.args
        q = query_parameters.get('q')
        coll = collection()
        df = pd.DataFrame(list(coll.find({})))
        temp = difflib.get_close_matches(q, df['fullAddress'])
        df = pd.DataFrame(list(coll.find({'fullAddress': temp[0]})))
        print(temp)
        if df.empty:
            return page_not_found()
        else:
            df = df.drop(columns='_id')
            temp = df.to_json(orient='records', force_ascii=False)
            parsed = json.loads(temp)
            data =  json.dumps(parsed, indent=4, ensure_ascii=False)
            response = make_response(data)
            response.headers['Content-Type'] = 'application/json'
        
            return  response
    except:
        raise
        return internal_server_error()





