import pandas as pd
import numpy as np
import csv
import getTinh
#chỉ cần thay đổi tên file đầu vào là được
#Goi lệnh: python sliptAddress.py
fileName = 'eduHcmEncoding.csv'

df = pd.read_csv(fileName)

fileNameResult = fileName[0:len(fileName) - 4] + 'Result.csv'

#Thêm cột tỉnh, quận/huyện, xã/phường, đường
df['province'] = df['provinceCode'] = ''
df['district'] = df['districtCode'] = ''
df['village']  = df['villageCode'] = ''
df['street']   = df['streetCode'] = ''

for index, row in df.iterrows():
    addr = df.at[index, 'address']
    df.at[index, 'province'] = getTinh.getProvince(addr)
    df.at[index, 'provinceCode'] = getTinh.getProvinceCode(addr)
    df.at[index, 'district'] = getTinh.getDistrict(addr)
    df.at[index, 'districtCode'] = getTinh.getDistrictCode(addr)
    df.at[index, 'village'] = getTinh.getVillage(addr)
    df.at[index, 'villageCode'] = getTinh.getVillageCode(addr)
    df.at[index, 'street'] = getTinh.getStreet(addr)
    df.at[index, 'streetCode'] = getTinh.getStreetCode(addr)

df.to_csv(fileNameResult,index=False, encoding='utf-8-sig')
