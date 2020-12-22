import pandas as pd
import json
import difflib
from flask import request, jsonify, make_response, Blueprint
import connectionDB as connDB
areas = Blueprint('areas', __name__)


nameDB = 'SuccessfullLand_DB'
nameColl = 'areas'


#tạo kết nối tới DB và trả ra collection
def collection():
    db = connDB.connectionDBAtlas2(nameDB)
    coll = db[nameColl]
    return coll

@areas.errorhandler(404)
def page_not_found():
    data = {
            "statusCode": 404,
            "error": "Not Found",
            "message": "The resource could not be found."
        }
    return json.dumps(data), 404

@areas.errorhandler(500)
def internal_server_error():
    data = {
            "statusCode": 500,
            "error": "Internal Server Error",
            "message": "The server has encountered a situation it doesn't know how to handle."
        }
    return json.dumps(data), 500

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
    

#tìm kiếm khu vực do người dùng nhập vào
"""
    input: Get: http://127.0.0.1:5000/areas/search?q=Hồ Chí Minh
        Params: 
            q: là tên khu vực
                Ví dụ: q = Hồ Chí minh    => là khu vực Hồ chí minh
                       q = Phường 5, quận 3, hồ chi minh

            Lưu ý: tỉnh thì không cần ghi Tỉnh vào


    output: Khu vực cần hiển thị

"""
@areas.route('/areas/search', methods=['GET'])
def search():
    try:
        query_parameters = request.args
        q = query_parameters.get('q')
        q = q.replace('Tỉnh ','').replace('tỉnh ','')
        if not q:
            return page_not_found()
        coll = collection()
        df = pd.DataFrame(list(coll.find({})))
        temp = difflib.get_close_matches(q, df['fullAddress'])
        df = pd.DataFrame(list(coll.find({'fullAddress': temp[0]})))
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


#tìm kiếm danh sách 6 khu vực do người dùng nhập vào
"""
    input: Get: http://127.0.0.1:5000/areas/search_many?q= Quận 3
        Params: 
            q: là tên khu vực
            Ví dụ: Quận 3    => xuất danh sách tối đa là 6 khu vực liên quan đến quận 3
                             Phường 5, quận 3, hồ chi minh
            

    output: danh sách các khu vực được truyền vào params q (Danh sách có tối đa 6 khu vực)

"""
@areas.route('/areas/search_many', methods=['GET'])
def search_many():
    try:
        query_parameters = request.args
        q = query_parameters.get('q')
        if not q:
            return page_not_found()
        q = q.replace('Tỉnh ','').replace('tỉnh ','')
        coll = collection()
        df = pd.DataFrame(list(coll.find({"fullAddress": {"$regex" : ".*" + q + ".*"}}).limit(6)))
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





