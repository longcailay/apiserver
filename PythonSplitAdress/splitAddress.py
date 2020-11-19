import pandas as pd
import numpy as np
import csv
import re
import getTinh
#chỉ cần thay đổi tên file đầu vào là được
#Goi lệnh: python sliptAddress.py
fileName = 'hcm_restaurant.csv'

df = pd.read_csv(fileName)

fileNameResult = fileName[0:len(fileName) - 4] + 'Result.csv'

#Thêm cột tỉnh, quận/huyện, xã/phường, đường
df['province'] = df['provinceCode'] = ''
df['district'] = df['districtCode'] = ''
df['village']  = df['villageCode'] = ''
df['street']   = df['streetCode'] = ''

for index, row in df.iterrows():
    addr = df.at[index, 'address']
    location = re.findall(r"[-+]?\d*\.\d+|\d+", df.at[index, 'gps'])
    lat = location[0]
    lon = location[1]
    df.at[index, 'province'] = getTinh.getProvince(addr)
    df.at[index, 'provinceCode'] = getTinh.getProvinceCode(addr)
    df.at[index, 'district'] = getTinh.getDistrict(addr)
    df.at[index, 'districtCode'] = getTinh.getDistrictCode(addr)
    df.at[index, 'village'] = getTinh.getVillage(addr,lat,lon)
    df.at[index, 'villageCode'] = getTinh.getVillageCode(addr,lat,lon)
    df.at[index, 'street'] = getTinh.getStreet(addr)
    df.at[index, 'streetCode'] = getTinh.getStreetCode(addr)

df.to_csv(fileNameResult,index=False, encoding='utf-8-sig')
