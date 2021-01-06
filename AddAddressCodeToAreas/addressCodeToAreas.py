import pandas as pd
import csv
import json
from unidecode import unidecode

df = pd.read_json(r'areas.json', encoding='utf-8-sig')


def addressToCode(address):
    if isinstance(address,float):
        address = ''
    #print(type(address))
    result = str(address)
    result = unidecode(address).strip()
    result = result.replace(',','').replace('  ',' ').replace('  ',' ').replace('  ',' ').replace(' - ', ' ')
    result = result.lower()
    return result


#Thêm cột fullAddressCode
for index, row in df.iterrows():
    tempAddress = df.at[index, 'fullAddress']
    strFullAddressCode = addressToCode(tempAddress)
    df.at[index, 'fullAddressCode'] = strFullAddressCode


# #Thêm cột pro_districtCode
# for index, row in df.iterrows():
#     if index >= 714:
#         break
#     tempID = df.at[index, 'pro_districtID']
#     strProvinceCode = IDToCodeProvince(dfProvince, tempID)
#     df.at[index, 'pro_districtCode'] = strProvinceCode




# for index, row in df.iterrows():
#     #them data vao 3 cot: provinceCode, districtCode, villageCode
#     strProvince = df.at[index, 'province']
#     df.at[index, 'provinceCode'] = addressToCode(strProvince)
#     strDistrict = df.at[index, 'district']
#     df.at[index, 'districtCode'] = addressToCode(strDistrict)
#     strVillage = df.at[index, 'village']
#     df.at[index, 'villageCode'] = addressToCode(strVillage)

print(df)
df.to_json('areasCodeAddress.json', orient='records')