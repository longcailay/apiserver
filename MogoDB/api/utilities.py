import pandas as pd
import json
import difflib
from flask import request, jsonify, make_response, Blueprint

import connectionDB as connDB
utilities = Blueprint('utilities', __name__)

nameDB = 'SuccessfullLand_DB'
nameColl = 'utilities'

#tạo kết nối tới DB và trả ra collection
def collection():
    db = connDB.connectionDBAtlas2(nameDB)
    coll = db[nameColl]
    return coll

@utilities.errorhandler(404)
def page_not_found():
    data = {
            "statusCode": 404,
            "error": "Not Found",
            "message": "The resource could not be found."
        }
    return json.dumps(data), 404

@utilities.errorhandler(500)
def internal_server_error():
    data = {
            "statusCode": 500,
            "error": "Internal Server Error",
            "message": "The server has encountered a situation it doesn't know how to handle."
        }
    return json.dumps(data), 500


#Tìm kiếm các utilities theo tham số vào
"""
    input: Get: http://127.0.0.1:5000/utilities
        Params:
            category: loại tiện ích (string)
                    VD: "Nhà hàng", "Giáo dục", "Bệnh viện"
                    hoặc "all", là tất cả các tiện ích trong khu vực

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
        
        if not (category or lat_1 or lat_2 or lon_1 or lon_2):
            return page_not_found()
        coll = collection()
        if category != 'all':
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
        else:
            df = pd.DataFrame(list(coll.find(
                {
                    "$and":[
                        {"gps.latitude": {"$lt": lat_1}},
                        {"gps.latitude": {"$gt": lat_2}},
                        {"gps.longitude": {"$gt": lon_1}},
                        {"gps.longitude": {"$lt": lon_2}}
                    ]                
                }
            )))
        if df.empty:
            data = []
            return json.dumps(data), 200
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


#Thống kê số lượng tiện ích cho 1 khu vực
"""
    input: Get: http://127.0.0.1:5000/utilities/counts
        Params:
            type_area: loại khu vực
                   1 - Tỉnh
                   2 - Huyện, quận
                   3 - Xã phường

            category: loại tiện ích (string)
                    VD: "Nhà hàng", "Giáo dục", "Bệnh viện"
                    hoặc "all", là tất cả các tiện ích trong khu vực

            province_code: mã Tỉnh
                VD: ho-chi-minh, tien-giang,...

            district_code: mã quận/huyện
                VD: quan-1, huyen-binh-chanh,...

            village_code: mã xã/phường
                VD: phuong-7, xa-tan-phu,...
            

    output: kết quả thống kê số lượng tiện ích trong khu vực
            vd:
                {
                    type_area: 1,
                    province: ho-chi-minh,
                    counts:{
                        "Giáo dục": 2,
                        "Nhà hàng": 4,
                        "Bệnh viện": 7
                    }
                }

"""
@utilities.route('/utilities/counts', methods=['GET'])
def utilities_counts():
    try:
        query_params = request.args

        type_area = query_params.get('type_area')

        result = {}
        if type_area == "1": #là tỉnh
            category = query_params.get('category')
            province = query_params.get('province')

            if category != "all":
                result = {
                            "type_area": 1,
                            "province": province,
                            "counts":{
                                category: "abc"
                            }
                        }
                        
            data =  json.dumps(result, indent=4, ensure_ascii=False)
            response = make_response(data)
            response.headers['Content-Type'] = 'application/json'
            return  response
    except:
        return internal_server_error()
