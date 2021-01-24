import pandas as pd
import json
import difflib
from flask import request, jsonify, make_response, Blueprint

import connectionDB as connDB
price = Blueprint('price', __name__)

nameDB = 'LongHoDB'

#tạo kết nối tới DB và trả ra collection
def collection(nameColl):
    db = connDB.connectionDBAtlas3(nameDB)
    coll = db[nameColl]
    return coll

@price.errorhandler(404)
def page_not_found():
    data = {
            "statusCode": 404,
            "error": "Not Found",
            "message": "The resource could not be found."
        }
    return json.dumps(data), 404

@price.errorhandler(500)
def internal_server_error():
    data = {
            "statusCode": 500,
            "error": "Internal Server Error",
            "message": "The server has encountered a situation it doesn't know how to handle."
        }
    return json.dumps(data), 500


#Tìm kiếm danh sách các thể loại bất động sản
"""
    input: Get: http://47.241.7.27:5000/price_category

    output: danh sách tất cả các thể loại bất động sản đang hổ trợ

"""
@price.route('/<price_category>', methods=['GET'])
def price_category(price_category):
    try:
        if price_category != 'price_category':
            return page_not_found()
        coll = collection('price_category')
        df = pd.DataFrame(list(coll.find({})))
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


def getYearId(year):
    year = int(year)
    year_id = -1
    if year == 2015:
        year_id = 0
    if year == 2016:
        year_id = 1
    if year == 2017:
        year_id = 2
    if year == 2018:
        year_id = 3
    if year == 2019:
        year_id = 4
    return year_id

#Trả ra API về giá cần thiết để làm biểu đồ
"""
    input: Get: http://47.241.7.27:5000/price
        Params:
            type: 1,2,3 là tỉnh, huyện, hoặc xã (type của areas)

            provinceCode: mã Tỉnh
                VD: ho-chi-minh, tien-giang,...

            districtCode: mã quận/huyện
                VD: quan-1, huyen-binh-chanh,...

            villageCode: mã xã/phường
                VD: phuong-7, xa-tan-phu,...    


            category_id: id loại bất động sản (integer) (từ 0 -> 15)
                    VD: id của mấy cái loại như "Bán căn hộ chung cư"

                    có thể bằng "all" nghĩa là tất cả các loại bất động sản

            year: năm cần thống kê về giá (hiện tại year nằm trong khoản 2015 - 2019)
                    year = "all", thì giá sẽ được xuất theo trung bình của các năm: 2015,2016,2017,2018,2019
                    nếu 2015 <= year <= 2019, thì giá sẽ được xuất theo trung bình tháng của năm đó: (12 cột tương ứng 12 tháng)



    Output: Api về giá tương ứng các tham số truyền vào

"""
@price.route('/price', methods=['GET'])
def get_price():
    try:
        query_params = request.args

        type_area = query_params.get('type')
        province_code = query_params.get('provinceCode')
        district_code = query_params.get('districtCode')
        village_code = query_params.get('villageCode')

        category_id = query_params.get('category_id')
        year = query_params.get('year')
        

        #initialize variable
        year_id = 0

        df = None
        coll = None

        query = {}
        projection = {}

        #check params
        if not (type_area or province_code or category_id or year):
            return page_not_found()

        if year not in ["2015", "2016", "2017", "2018", "2019", "all"]:
            return page_not_found()
        else:
            if year != "all":
                year_id = getYearId(year)

        if type_area not in ["1","2","3"]:
            return page_not_found()

        temp = ["0"]
        for i in range(1,17):
            temp.append(str(i))
        temp.append("all")
   
        if category_id not in temp:
            return page_not_found()
        else:
            if category_id != "all":
                category_id = int(category_id)
        

        # 3 trường hợp lớn về khu vực (query)
        if type_area == "1": #là tỉnh
            coll = collection('price_province')
            df = pd.DataFrame(list(coll.find({"provinceCode": province_code})))

        if type_area == "2": #là huyện
            #check params district
            if not district_code:
                return page_not_found()
            coll = collection('price_district')
            query = {"provinceCode": province_code, "districtCode": district_code}

        if type_area == "3": # là phường xã
            #check params village
            if not (district_code or village_code):
                return page_not_found()
            coll = collection('price_village')
            query = {"provinceCode": province_code, "districtCode": district_code, "villageCode": village_code}


        # 4 trường hợp lớn về year và category_id
        #1 year != "all" and category_id != "all"
        if year != "all" and category_id != "all":
            projection = {"category": {"$slice":[category_id,1]}, "category.average_price_year": {"$slice":[year_id,1]}}
        
        #2 year != "all" and category_id == "all"
        if year != "all" and category_id == "all":
            projection = {"category.average_price_year": {"$slice":[year_id,1]}}

        #3 year == "all" and category_id == all
        if year == "all" and category_id == "all":
            projection = {"category.average_price_year.average_price_month": 0}

        #4 year == "all" and category_id != "all"
        if year == "all" and category_id != "all":
            projection = {"category.average_price_year.average_price_month": 0,"category": {"$slice":[category_id,1]}}




        df = pd.DataFrame(list(coll.find(query, projection)))

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
