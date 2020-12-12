import flask
import pandas as pd
import json
import csv
import difflib
from flask import request, jsonify, make_response, Blueprint


import connectionDB as connDB
utilities = Blueprint('utilities', __name__)

nameDB = 'SuccessfullLand_DB'
nameColl = 'utilities'

#tạo kết nối tới DB và trả ra collection
def collection():
    db = connDB.connectionDBAtlas(nameDB)
    coll = db[nameColl]
    return coll

@utilities.errorhandler(404)
def page_not_found():
    return "<h1>404 Not Found</h1><p>The resource could not be found.</p>", 404

@utilities.errorhandler(500)
def internal_server_error():
    return "<h1>500 Internal Server Error</h1><p>The server has encountered a situation it doesn't know how to handle.</p>", 500


#Tìm kiếm các utilities theo tham số vào
"""
    input: Get: http://127.0.0.1:5000/utilities
        Params:
            category: loại tiện ích (string)
                    VD: "Nhà hàng", "Giáo dục", "Bệnh viện"
                    hoặc "All", là tất cả các tiện ích trong khu vực

            lat_1: latitude điểm trái trên (float)
            lon_1: longitude điểm trái trên (float)
            lat_2: latitude điểm phải dưới (float)
            lon_2: longitude điểm phải dưới (float)
            

    output: danh sách tất cả các tiện ích trong khu vực tọa độ đó theo thể loại

"""
@utilities.route('/utilities', methods=['GET'])
def utilities_filter():
    try:
        query_params = request.args

        category = query_params.get('category')

        lat_1 = float(query_params.get('lat_1'))
        lon_1 = float(query_params.get('lon_1'))
        lat_2 = float(query_params.get('lat_2'))
        lon_2 = float(query_params.get('lon_2'))
        

        coll = collection()
        df = pd.DataFrame(list(coll.find(
            {
                "$and":[
                    {"gps.latitude": {"$lt": lat_1}},
                    {"gps.latitude": {"$gt": lat_2}},
                    {"gps.longitude": {"$gt": lon_1}},
                    {"gps.longitude": {"$lt": lon_2}},
                    {"category": category}
                ]                
            }
        )))
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
