import pandas as pd
import numpy as np
import math
import csv
from unidecode import unidecode

def addressToCode(address):
    if isinstance(address,float):
        address = ''
    #print(type(address))
    result = str(address)
    result = unidecode(address).strip()
    result = result.replace(' - ','-').replace(' ','-').replace('  ','-').replace('  ','-').replace('  ','-').replace('--','-').replace('--','-').replace('--','-')
    result = result.lower()
    return result


#chỉ cần thay đổi tên file đầu vào là được
#Goi lệnh: python addInfoAddress.py
fileName = 'address.csv'

df = pd.read_csv(fileName)


#Thêm cột tỉnh, quận/huyện, xã/phường, đường
df['provinceCode'] = ''
df['districtCode'] = ''
df['villageCode'] = ''
df['pro_districtCode'] = ''
df['dis_villageCode'] = ''

fileNameResult = fileName[0:len(fileName) - 4] + 'Result.csv'



for index, row in df.iterrows():
    #them data vao 3 cot: provinceCode, districtCode, villageCode
    strProvince = df.at[index, 'province']
    df.at[index, 'provinceCode'] = addressToCode(strProvince)
    strDistrict = df.at[index, 'district']
    df.at[index, 'districtCode'] = addressToCode(strDistrict)
    strVillage = df.at[index, 'village']
    df.at[index, 'villageCode'] = addressToCode(strVillage)


dfProvince = df.loc[df["serial"] <= 63, ["province","provinceID","provinceCode"]]#tạo subDataframe từ df có 3 cột với điều kiện serial trong df <= 63
dfDistrict = df.loc[df["districtID"] <= 99999, ["district", "districtID", "districtCode"]]

def IDToCodeProvince(subDf, ID):
    dfResult = subDf.loc[subDf["provinceID"] == ID, ["provinceCode"]]
    result = dfResult['provinceCode'].values[0] #lấy giá trị tại dòng đầu tiên của cột
    return result

def IDToCodeDistrict(subDf, ID):
    dfResult = subDf.loc[subDf["districtID"] == ID, ["districtCode"]]
    result = dfResult['districtCode'].values[0] #lấy giá trị tại dòng đầu tiên của cột
    return result

#Thêm cột pro_districtCode
for index, row in df.iterrows():
    if index >= 714:
        break
    tempID = df.at[index, 'pro_districtID']
    strProvinceCode = IDToCodeProvince(dfProvince, tempID)
    df.at[index, 'pro_districtCode'] = strProvinceCode

#Thêm cột dis_villageCode
for index, row in df.iterrows():
    if index >= 11557:
        break
    tempID = df.at[index, 'dis_villageID']
    strDistrictCode = IDToCodeDistrict(dfDistrict,tempID)
    df.at[index, 'dis_villageCode'] = strDistrictCode

df.to_csv(fileNameResult,index=False, encoding='utf-8-sig')

