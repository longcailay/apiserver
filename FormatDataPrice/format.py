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

fileName = 'Hồ Chí Minh_Quận 6_new.csv'

df = pd.read_csv(fileName)

df = df.loc[ not (df["Price"]).empty and not (df['Area']).empty, ["Level1", "Level2", "Level3","Category","CateName","PriceValue","AreaValue","AveragePrice","Time"]]




#Thêm cột tỉnh, quận/huyện, xã/phường, đường
df['provinceCode'] = ''
df['districtCode'] = ''
df['villageCode'] = ''

fileNameResult = fileName[0:len(fileName) - 8] + 'Result.csv'

df.to_csv(fileNameResult,index=False, encoding='utf-8-sig')