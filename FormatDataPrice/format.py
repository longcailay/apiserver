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

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def processFile(df):
    df = df.loc[ (df["Level1"] == "Hồ Chí Minh") & (df["AveragePrice"] != 0), ["Level1", "Level2", "Level3","Category","CateName","PriceValue","AreaValue","AveragePrice","Time"]]

    #Thêm cột tỉnh, quận/huyện, xã/phường, đường
    df['provinceCode'] = ''
    df['districtCode'] = ''
    df['villageCode'] = ''
    for index, row in df.iterrows():
        temp1 = df.at[index, 'Level1']
        temp2 = df.at[index, 'Level2']
        temp3 = df.at[index, 'Level3']

        if str(temp3).find('Phường') == -1:
            temp3 = 'Phường ' + temp3
        else:
            if len(str(temp3)) == 8 and hasNumbers(str(temp3)):
                t1 = temp3[0:7]
                t2 = temp3[7:8]
                temp3 = t1 + '0' + t2

        df.at[index, 'provinceCode'] = addressToCode(temp1)
        df.at[index, 'districtCode'] = addressToCode(temp2)
        df.at[index, 'villageCode'] = addressToCode(temp3)
    return df

for i in range(6,7):
    fileName = 'Hồ Chí Minh_Quận ' + str(i) + '_new.csv'
    df = pd.read_csv(fileName)
    df = processFile(df)
    fileNameResult = fileName[0:len(fileName) - 8] + 'Result.csv'

    df.to_csv(fileNameResult,index=False, encoding='utf-8-sig')




